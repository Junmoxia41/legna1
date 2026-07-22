"""Fast local intent classifier used before involving an LLM."""
from typing import Dict, List


class IntentClassifier:
    RULES = {
        "code": ("código", "codigo", "python", "javascript", "error", "bug", "función", "funcion", "programa", "script", "github", "git", "api"),
        "research": ("pdf", "documento", "resume", "resumen", "investiga", "buscar", "artículo", "articulo", "fuente", "analiza este archivo"),
        "planner": ("plan", "organiza", "organizar", "objetivo", "tarea", "calendario", "prioridad", "proyecto", "pasos"),
        "memory": ("recuerda", "recordar", "mi nombre", "prefiero", "guarda", "memoria", "olvida"),
        "system": ("cpu", "ram", "sistema", "proceso", "equipo", "gpu", "rendimiento", "temperatura"),
        "vision": ("imagen", "foto", "captura", "screenshot", "visual", "ves en"),
        "documents": ("pdf", "docx", "excel", "csv", "documento", "archivo"),
        "data": ("datos", "tabla", "dataset", "csv", "gráfica", "grafica", "estadística"),
        "security": ("seguridad", "permiso", "token", "contraseña", "vulnerabilidad", "riesgo"),
    }

    def classify(self, message: str) -> Dict:
        text = message.lower()
        matched: List[str] = []
        for intent, keywords in self.RULES.items():
            if any(keyword in text for keyword in keywords):
                matched.append(intent)
        if not matched:
            matched = ["core"]
        # Core is always responsible for response synthesis, not a duplicate worker.
        agents = ["core"] + [item for item in matched if item != "core"]
        if "quality" not in agents:
            agents.append("quality")
        return {"primary": matched[0], "agents": agents, "confidence": 0.8 if len(matched) else 0.45}
