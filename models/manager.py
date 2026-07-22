"""Catalogs GGUF files, model assignments, and at most two logical active slots."""
import json
import shutil
from pathlib import Path
from typing import Dict
from models.reliability import ModelReliabilityStore
from models.router import ModelRouter
from models.scanner import ModelScanner
from models.runtime import RuntimeManager


class ModelManager:
    MAX_ACTIVE_SLOTS = 2

    def __init__(self, models_dir=None):
        directory = Path(models_dir) if models_dir else Path(__file__).resolve().parents[1] / "data" / "models"
        self.scanner = ModelScanner(directory)
        self.runtime_manager = RuntimeManager()
        self.reliability = ModelReliabilityStore()
        self.router = ModelRouter(self.reliability)
        self.assignments_path = self.scanner.models_dir.parent / "agent_model_assignments.json"
        self.assignments = self._load_assignments()
        self._slots = [{"slot": 1, "purpose": "Core / General", "model": None}, {"slot": 2, "purpose": "Especialista dinámico", "model": None}]

    def _load_assignments(self):
        try: return json.loads(self.assignments_path.read_text(encoding="utf-8"))
        except (OSError, ValueError): return {}

    def _save_assignments(self):
        self.assignments_path.write_text(json.dumps(self.assignments, indent=2, ensure_ascii=False), encoding="utf-8")

    def import_gguf(self, source_path):
        source = Path(source_path)
        if not source.is_file() or source.suffix.lower() != ".gguf": raise ValueError("Selecciona un archivo GGUF válido.")
        destination = self.scanner.models_dir / source.name
        if destination.resolve() != source.resolve():
            if destination.exists(): raise FileExistsError("Ya existe un modelo con ese nombre.")
            shutil.copy2(source, destination)
        models = self.scanner.scan()
        return next((model for model in models if model["path"] == str(destination)), None)

    def assign_agent(self, agent_id, model_id):
        available = {model["id"] for model in self.scanner.scan()}
        runtime_models = {model for runtime in self.runtime_manager.discover() for model in runtime["models"]}
        if model_id not in available and model_id not in runtime_models and model_id != "auto":
            raise ValueError("El modelo seleccionado no está disponible en el catálogo.")
        self.assignments[agent_id] = model_id
        self._save_assignments()
        return model_id

    def select_for_task(self, task_type: str) -> Dict:
        runtimes = self.runtime_manager.discover()
        active = next((item for item in runtimes if item["status"] == "online"), None)
        available = active["models"] if active else []
        ranking = self.router.choose(task_type, available) if available else []
        selected = ranking[0]["model_id"] if ranking else None
        return {"runtime": active["id"] if active else None, "model": selected, "ranking": ranking}

    def record_outcome(self, model_id: str, task_type: str, score: float, source="automatic"):
        return self.reliability.record(model_id, task_type, score, source) if model_id else None

    def dashboard(self) -> Dict:
        catalog = self.scanner.scan(); runtimes = self.runtime_manager.discover()
        active = next((item for item in runtimes if item["status"] == "online"), None)
        runtime_models = active["models"] if active else []
        ratings = [self.reliability.rating(model_id, "general") for model_id in runtime_models]
        options = [{"id": "auto", "name": "AUTO · Router de LEGNA"}] + [{"id": model["id"], "name": model["name"]} for model in catalog] + [{"id": model, "name": model} for model in runtime_models if model not in {entry["id"] for entry in catalog}]
        return {"models_dir": str(self.scanner.models_dir), "catalog": catalog, "runtimes": runtimes, "active_runtime": active["id"] if active else None, "slots": self._slots, "max_active_slots": self.MAX_ACTIVE_SLOTS, "ratings": ratings, "assignments": self.assignments, "options": options}
