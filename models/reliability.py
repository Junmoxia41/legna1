"""Persistent evidence-based reputation for local model/runtime combinations."""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class ModelReliabilityStore:
    def __init__(self, path=None):
        self.path = Path(path) if path else Path(__file__).resolve().parents[1] / "data" / "model_reliability.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self):
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {"models": {}}

    def _save(self):
        self.path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")

    def record(self, model_id: str, task_type: str, score: float, source: str = "automatic") -> Dict:
        """Store score 0..1 using an evidence-weighted average, not raw self-rating."""
        score = max(0.0, min(1.0, float(score)))
        key = f"{model_id}::{task_type}"
        entry = self.data["models"].setdefault(key, {"model_id": model_id, "task_type": task_type, "score": 0.60, "samples": 0, "successes": 0, "failures": 0, "last_updated": None})
        # First scores move reputation visibly; later evidence stabilizes it.
        weight = min(entry["samples"], 12)
        entry["score"] = round((entry["score"] * weight + score) / (weight + 1), 3)
        entry["samples"] += 1
        entry["successes"] += int(score >= 0.6)
        entry["failures"] += int(score < 0.4)
        entry["last_updated"] = datetime.now().isoformat()
        entry["last_source"] = source
        self._save()
        return entry

    def rating(self, model_id: str, task_type: str) -> Dict:
        entry = self.data["models"].get(f"{model_id}::{task_type}")
        if not entry:
            return {"model_id": model_id, "task_type": task_type, "score": 0.60, "stars": 3.0, "samples": 0}
        result = dict(entry)
        result["stars"] = round(1 + result["score"] * 4, 1)
        return result

    def leaderboard(self, task_type: str, candidates: List[str]) -> List[Dict]:
        return sorted((self.rating(model, task_type) for model in candidates), key=lambda item: item["score"], reverse=True)
