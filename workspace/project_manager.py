"""
Project Manager for Legna Workspace
Handles creation, import, and management of projects.
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class ProjectManager:
    def __init__(self, workspace_root=None):
        self.workspace_root = Path(workspace_root) if workspace_root else Path(__file__).resolve().parent / "workspace"
        self.projects_dir = self.workspace_root / "projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata_file = self.workspace_root / "projects_metadata.json"
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict:
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {"projects": []}
        return {"projects": []}

    def _save_metadata(self):
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)

    def create_new_project(self, name: str, description: str = "") -> Dict:
        """Create a new empty project folder"""
        project_path = self.projects_dir / name
        project_path.mkdir(exist_ok=True)
        
        # Create basic structure
        (project_path / "src").mkdir(exist_ok=True)
        (project_path / "docs").mkdir(exist_ok=True)
        main_file = project_path / "src" / "main.py"
        readme_file = project_path / "README.md"
        if not main_file.exists():
            main_file.write_text(
                "def main():\n"
                "    print('LEGNA workspace listo')\n\n\n"
                "if __name__ == '__main__':\n"
                "    main()\n",
                encoding="utf-8",
            )
        if not readme_file.exists():
            readme_file.write_text(f"# {name}\n\nProyecto creado con LEGNA IDE.\n", encoding="utf-8")
        
        project_data = {
            "id": str(datetime.now().timestamp()),
            "name": name,
            "path": str(project_path),
            "description": description,
            "created_at": datetime.now().isoformat(),
            "file_count": 2,
            "size_mb": round(sum(item.stat().st_size for item in project_path.rglob("*") if item.is_file()) / (1024 * 1024), 2),
            "type": "new"
        }
        
        self.metadata["projects"].append(project_data)
        self._save_metadata()
        return project_data

    def import_project(self, source_path: str, move: bool = True, new_name: Optional[str] = None) -> Dict:
        """
        Import an external project.
        - move=True  → moves the folder into workspace/projects/
        - move=False → creates a reference (keeps original location)
        """
        source = Path(source_path).resolve()
        if not source.exists() or not source.is_dir():
            raise ValueError(f"Invalid project path: {source_path}")

        project_name = new_name or source.name
        target_path = self.projects_dir / project_name

        if move:
            # Move the entire folder
            if target_path.exists():
                target_path = self.projects_dir / f"{project_name}_{int(datetime.now().timestamp())}"
            shutil.move(str(source), str(target_path))
            location = "moved"
        else:
            # Keep original location + create reference
            target_path = source
            location = "referenced"

        # Count files
        file_count = sum(1 for _ in target_path.rglob("*") if _.is_file())
        size_mb = sum(f.stat().st_size for f in target_path.rglob("*") if f.is_file()) / (1024 * 1024)

        project_data = {
            "id": str(datetime.now().timestamp()),
            "name": project_name,
            "path": str(target_path),
            "original_path": str(source) if not move else None,
            "description": f"Proyecto importado - {location}",
            "created_at": datetime.now().isoformat(),
            "file_count": file_count,
            "size_mb": round(size_mb, 2),
            "type": "imported",
            "location_type": location
        }

        self.metadata["projects"].append(project_data)
        self._save_metadata()
        return project_data

    def get_all_projects(self) -> List[Dict]:
        return self.metadata.get("projects", [])

    def get_project(self, project_id: str) -> Optional[Dict]:
        for p in self.metadata.get("projects", []):
            if p["id"] == project_id:
                return p
        return None

    def delete_project(self, project_id: str, delete_files: bool = False):
        project = self.get_project(project_id)
        if not project:
            return False

        if delete_files and project.get("location_type") == "moved":
            try:
                shutil.rmtree(project["path"])
            except:
                pass

        self.metadata["projects"] = [p for p in self.metadata["projects"] if p["id"] != project_id]
        self._save_metadata()
        return True

    def scan_project_files(self, project_id: str) -> List[str]:
        """Returns list of relative file paths"""
        project = self.get_project(project_id)
        if not project:
            return []
        
        base = Path(project["path"])
        files = []
        for f in base.rglob("*"):
            if f.is_file():
                try:
                    rel = str(f.relative_to(base))
                    files.append(rel)
                except:
                    pass
        return files
