"""
Project Analyzer - Legna v2.0
Detects when user wants to analyze or modify a project from chat
"""

import os
from pathlib import Path
from workspace.project_manager import ProjectManager


class ProjectAnalyzer:
    def __init__(self):
        self.pm = ProjectManager()

    def detect_project_intent(self, message: str) -> dict:
        """
        Detects if the user wants to work with a project.
        Returns dict with action and project info.
        """
        msg = message.lower()
        
        keywords = ["analiza", "analizar", "modifica", "modificar", "abre", "abrir", 
                    "proyecto", "workspace", "editor", "código"]

        if any(kw in msg for kw in keywords):
            projects = self.pm.get_all_projects()
            
            for proj in projects:
                name = proj["name"].lower()
                if name in msg or "legna" in msg or "legna1" in msg:
                    return {
                        "action": "open_project",
                        "project": proj,
                        "message": f"Voy a abrir el proyecto **{proj['name']}** en el editor."
                    }
            
            # Generic project intent
            if "proyecto" in msg:
                return {
                    "action": "suggest_projects",
                    "message": "Tengo varios proyectos. ¿Cuál quieres que analice?"
                }

        return {"action": "none"}

    def get_project_suggestion(self):
        projects = self.pm.get_all_projects()
        if projects:
            return f"Tengo {len(projects)} proyectos disponibles. ¿Quieres que abra alguno?"
        return "Aún no tienes proyectos importados."
