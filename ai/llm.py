"""Client for local OpenAI-compatible runtimes with automatic failover."""
import requests

from config import LLAMA_CPP_URL, LM_STUDIO_URL, MODEL


class LLMClient:
    def __init__(self):
        self.model = MODEL
        self.endpoints = (
            ("lm_studio", "LM Studio", LM_STUDIO_URL),
            ("llama_cpp", "llama.cpp", LLAMA_CPP_URL),
        )

    def preguntar_con_meta(self, mensaje, model=None):
        """Try LM Studio first, then llama.cpp. Return response + execution evidence."""
        requested_model = model or self.model
        payload = {
            "model": requested_model,
            "messages": [{"role": "user", "content": mensaje}],
            "temperature": 0.7,
        }
        failures = []
        for runtime_id, runtime_name, url in self.endpoints:
            try:
                response = requests.post(url, json=payload, timeout=90)
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"].strip()
                if not content:
                    raise ValueError("Respuesta vacía")
                actual_model = data.get("model") or requested_model
                return {"ok": True, "response": content, "runtime": runtime_id,
                        "runtime_label": runtime_name, "model": actual_model, "failures": failures}
            except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as exc:
                failures.append({"runtime": runtime_id, "reason": exc.__class__.__name__})
        return {"ok": False, "response": "No puedo comunicarme con ningún runtime local. "
                "Inicia LM Studio en el puerto 1234 o llama.cpp en el puerto 8080.",
                "runtime": None, "model": requested_model, "failures": failures}

    def preguntar(self, mensaje):
        return self.preguntar_con_meta(mensaje)["response"]
