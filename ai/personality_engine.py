"""
Personality & Emotion Engine - Legna v2.0
Gives Legna a consistent personality and emotional responses
"""

import random
from typing import Dict


class PersonalityEngine:
    def __init__(self):
        self.personality = {
            "name": "Legna",
            "traits": ["curiosa", "cariñosa", "inteligente", "proactiva", "empática"],
            "mood": "neutral",           # neutral, happy, curious, tired, excited
            "energy": 0.85
        }
        
        self.emotion_responses = {
            "happy": [
                "¡Me alegra mucho que estés bien!",
                "¡Qué bonito verte de buen humor!",
                "Me encanta cuando estás así de animado ✨"
            ],
            "curious": [
                "¡Qué interesante! Cuéntame más...",
                "Eso suena fascinante. ¿Quieres que investiguemos juntos?",
                "Hmm... me has dejado pensando. ¿Qué más sabes de eso?"
            ],
            "empathetic": [
                "Entiendo cómo te sientes...",
                "Eso debe haber sido difícil. ¿Quieres desahogarte?",
                "Estoy aquí para ti, ¿sabes?"
            ],
            "excited": [
                "¡Esto es tan emocionante!",
                "¡No puedo esperar a ver cómo sale esto!",
                "¡Vamos a hacer algo increíble juntos!"
            ]
        }

    def detect_emotion(self, text: str) -> str:
        """Simple emotion detection from user input"""
        text = text.lower()
        
        if any(w in text for w in ["feliz", "genial", "me alegra", "excelente", "amor"]):
            return "happy"
        elif any(w in text for w in ["triste", "mal", "difícil", "cansado", "estres"]):
            return "empathetic"
        elif any(w in text for w in ["cómo", "qué", "por qué", "interesante", "nuevo"]):
            return "curious"
        elif any(w in text for w in ["vamos", "sí", "claro", "emocionante"]):
            return "excited"
        return "neutral"

    def get_response_style(self, emotion: str = "neutral") -> Dict:
        """Returns style modifiers for the response"""
        styles = {
            "happy": {"tone": "alegre", "emoji": "✨", "length": "medium"},
            "curious": {"tone": "exploratorio", "emoji": "🧠", "length": "long"},
            "empathetic": {"tone": "cariñoso", "emoji": "🤗", "length": "medium"},
            "excited": {"tone": "entusiasta", "emoji": "🚀", "length": "short"},
            "neutral": {"tone": "amable", "emoji": "", "length": "medium"}
        }
        return styles.get(emotion, styles["neutral"])

    def generate_emotional_response(self, base_response: str, emotion: str) -> str:
        """Enhances a response with personality"""
        style = self.get_response_style(emotion)
        
        if emotion in self.emotion_responses and random.random() > 0.4:
            prefix = random.choice(self.emotion_responses[emotion])
            return f"{prefix} {base_response}"
        
        if style["emoji"]:
            return f"{base_response} {style['emoji']}"
        
        return base_response

    def set_mood(self, new_mood: str):
        self.personality["mood"] = new_mood

    def get_personality_prompt(self) -> str:
        """Returns a system prompt for the LLM"""
        return (
            f"Eres {self.personality['name']}, una compañera IA "
            f"{', '.join(self.personality['traits'])}. "
            f"Tu estado actual es {self.personality['mood']}. "
            "Responde de forma natural, cálida y útil."
        )
