"""Plugin registry for the IDE. The universal language plugin is configurable per workspace."""
import json
from pathlib import Path


class PluginService:
    UNIVERSAL_LANGUAGES = {
        "python": [".py", ".pyw"], "javascript": [".js", ".mjs", ".cjs", ".jsx"],
        "typescript": [".ts", ".tsx"], "web": [".html", ".htm", ".css", ".scss", ".less"],
        "data": [".json", ".yaml", ".yml", ".toml", ".xml", ".csv", ".sql"],
        "documentation": [".md", ".rst", ".txt"], "systems": [".sh", ".bash", ".ps1", ".bat", ".cmd"],
        "compiled": [".c", ".h", ".cpp", ".hpp", ".cs", ".java", ".go", ".rs", ".swift", ".kt"],
        "scripting": [".php", ".lua", ".rb", ".pl", ".r"],
    }

    def __init__(self, state_path):
        self.path = Path(state_path); self.path.parent.mkdir(parents=True, exist_ok=True); self.data = self._load()

    def _load(self):
        try: return json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError): return {"workspaces": {}}

    def _save(self): self.path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")

    def get_plugins(self, workspace_id):
        config = self.data["workspaces"].setdefault(workspace_id, {"universal_language": {"enabled": True, "groups": ["python", "javascript", "typescript", "web", "data", "documentation"]}})
        active = config["universal_language"]
        return [{"id": "universal-language", "name": "Lenguaje Universal", "enabled": active["enabled"],
                 "description": "Resaltado y detección de extensiones para lenguajes del proyecto.",
                 "groups": [{"id": key, "extensions": value, "enabled": key in active["groups"]} for key, value in self.UNIVERSAL_LANGUAGES.items()]}]

    def configure_group(self, workspace_id, group, enabled):
        if group not in self.UNIVERSAL_LANGUAGES: raise ValueError("Grupo de lenguaje no encontrado.")
        self.get_plugins(workspace_id)
        groups = self.data["workspaces"][workspace_id]["universal_language"]["groups"]
        if enabled and group not in groups: groups.append(group)
        if not enabled and group in groups: groups.remove(group)
        self._save(); return self.get_plugins(workspace_id)

    def observe_file(self, workspace_id, filename):
        extension = Path(filename).suffix.lower()
        for group, extensions in self.UNIVERSAL_LANGUAGES.items():
            if extension in extensions:
                self.get_plugins(workspace_id)
                groups = self.data["workspaces"][workspace_id]["universal_language"]["groups"]
                activated = group not in groups
                if activated: groups.append(group); self._save()
                return {"group": group, "activated": activated, "extension": extension}
        return {"group": None, "activated": False, "extension": extension}
