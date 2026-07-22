"""Evidence-based router: chooses candidates by specialty and prior outcomes."""
from typing import Dict, List
from models.reliability import ModelReliabilityStore


class ModelRouter:
    def __init__(self, reliability=None):
        self.reliability = reliability or ModelReliabilityStore()

    @staticmethod
    def infer_type(model_id: str) -> str:
        name = model_id.lower()
        if any(word in name for word in ("coder", "code", "deepseek")):
            return "code"
        if any(word in name for word in ("vision", "llava", "vl")):
            return "vision"
        return "general"

    def choose(self, task_type: str, available_models: List[str]) -> List[Dict]:
        preferred_type = "code" if task_type == "code" else "vision" if task_type == "vision" else "general"
        compatible = [model for model in available_models if self.infer_type(model) == preferred_type]
        candidates = compatible or available_models
        return self.reliability.leaderboard(task_type, candidates)
