"""
Deep Project Analyzer - Legna v2.0
Analyzes project structure, detects key files, dependencies, and suggests improvements
"""

import os
from pathlib import Path
from typing import Dict, List
from workspace.project_manager import ProjectManager


class DeepProjectAnalyzer:
    def __init__(self):
        self.pm = ProjectManager()

    def analyze_project(self, project_id: str) -> Dict:
        """Performs deep analysis of a project"""
        project = self.pm.get_project(project_id)
        if not project:
            return {"error": "Proyecto no encontrado"}

        base_path = Path(project["path"])
        files = self.pm.scan_project_files(project_id)

        analysis = {
            "name": project["name"],
            "total_files": len(files),
            "size_mb": project.get("size_mb", 0),
            "main_files": [],
            "languages": {},
            "dependencies": [],
            "structure": {},
            "suggestions": []
        }

        # Detect languages and main files
        lang_map = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".html": "HTML",
            ".css": "CSS",
            ".md": "Markdown",
            ".json": "JSON",
            ".java": "Java"
        }

        for file in files:
            ext = Path(file).suffix.lower()
            if ext in lang_map:
                lang = lang_map[ext]
                analysis["languages"][lang] = analysis["languages"].get(lang, 0) + 1

            # Detect main files
            name = Path(file).name.lower()
            if name in ["main.py", "app.py", "index.js", "main.js", "index.html"]:
                analysis["main_files"].append(file)

        # Detect dependencies
        if (base_path / "requirements.txt").exists():
            try:
                with open(base_path / "requirements.txt") as f:
                    analysis["dependencies"] = [line.strip() for line in f if line.strip()]
            except:
                pass

        if (base_path / "package.json").exists():
            analysis["dependencies"].append("Node.js project")

        # Generate structure summary
        folders = set()
        for f in files:
            parts = Path(f).parts
            if len(parts) > 1:
                folders.add(parts[0])
        analysis["structure"]["top_folders"] = list(folders)[:5]

        # Smart suggestions
        suggestions = []
        if "Python" in analysis["languages"] and not analysis["dependencies"]:
            suggestions.append("Añade un requirements.txt para gestionar dependencias")
        if len(analysis["main_files"]) == 0:
            suggestions.append("Considera crear un archivo main.py o index.js")
        if analysis["total_files"] > 30:
            suggestions.append("El proyecto es grande. ¿Quieres que organice la estructura?")
        if "Python" in analysis["languages"]:
            suggestions.append("Puedo ayudarte a mejorar el código Python")

        analysis["suggestions"] = suggestions

        return analysis

    def get_analysis_summary(self, project_id: str) -> str:
        """Returns a human-readable summary"""
        analysis = self.analyze_project(project_id)
        if "error" in analysis:
            return analysis["error"]

        summary = f"**{analysis['name']}**\n"
        summary += f"- {analysis['total_files']} archivos\n"
        summary += f"- Lenguajes: {', '.join(analysis['languages'].keys())}\n"
        
        if analysis["main_files"]:
            summary += f"- Archivos principales: {', '.join(analysis['main_files'])}\n"
        
        if analysis["suggestions"]:
            summary += "\n**Sugerencias:**\n"
            for s in analysis["suggestions"]:
                summary += f"• {s}\n"

        return summary
