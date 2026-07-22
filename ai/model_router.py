"""
Model Router - Legna v2.0
Multi-model system for different tasks
Supports multiple local models (LM Studio, Ollama, etc.)
"""

from typing import Dict, Optional


class ModelRouter:
    """
    Routes different tasks to appropriate models.
    - fast: greetings, simple chat, context
    - powerful: deep analysis, complex reasoning
    - creative: personality, emotional responses
    """

    def __init__(self):
        self.models = {
            "fast": {
                "name": "mistral-7b-instruct",
                "endpoint": "http://localhost:1234/v1",  # LM Studio default
                "role": "Respuestas rápidas y conversacionales"
            },
            "powerful": {
                "name": "llama-3-70b",           # or any stronger local model
                "endpoint": "http://localhost:1234/v1",
                "role": "Análisis profundo y razonamiento complejo"
            },
            "creative": {
                "name": "phi-3-medium",
                "endpoint": "http://localhost:1234/v1",
                "role": "Personalidad y respuestas emocionales"
            }
        }
        
        self.current_model = "fast"

    def get_model_for_task(self, task: str) -> Dict:
        """
        Returns the best model for a given task.
        Tasks: greeting, chat, deep_analysis, emotion, project_analysis
        """
        if task in ["deep_analysis", "project_analysis", "complex_reasoning"]:
            return self.models["powerful"]
        elif task in ["emotion", "personality", "creative_response"]:
            return self.models["creative"]
        else:
            return self.models["fast"]

    def switch_model(self, model_key: str):
        if model_key in self.models:
            self.current_model = model_key
            return self.models[model_key]
        return None

    def get_all_models(self) -> Dict:
        return self.models

    def get_model_info(self, task: str) -> str:
        model = self.get_model_for_task(task)
        return f"Usando modelo {model['name']} ({model['role']})"
