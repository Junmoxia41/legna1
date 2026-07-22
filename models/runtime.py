"""OpenAI-compatible local runtimes: LM Studio first, llama.cpp fallback."""
from dataclasses import dataclass
from typing import Dict, List, Optional
import requests


@dataclass(frozen=True)
class RuntimeEndpoint:
    id: str
    label: str
    base_url: str


class RuntimeManager:
    def __init__(self, lm_studio_url="http://127.0.0.1:1234/v1", llama_cpp_url="http://127.0.0.1:8080/v1"):
        self.runtimes = (
            RuntimeEndpoint("lm_studio", "LM Studio (principal)", lm_studio_url.rstrip("/")),
            RuntimeEndpoint("llama_cpp", "llama.cpp (respaldo)", llama_cpp_url.rstrip("/")),
        )

    def discover(self) -> List[Dict]:
        result = []
        for runtime in self.runtimes:
            try:
                response = requests.get(f"{runtime.base_url}/models", timeout=1.5)
                response.raise_for_status()
                data = response.json().get("data", [])
                model_ids = [item.get("id", "unknown") for item in data]
                result.append({"id": runtime.id, "label": runtime.label, "url": runtime.base_url,
                               "status": "online", "models": model_ids})
            except (requests.RequestException, ValueError):
                result.append({"id": runtime.id, "label": runtime.label, "url": runtime.base_url,
                               "status": "offline", "models": []})
        return result

    def active_runtime(self) -> Optional[Dict]:
        return next((runtime for runtime in self.discover() if runtime["status"] == "online"), None)
