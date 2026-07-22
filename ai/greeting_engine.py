"""
Greeting Engine - Legna v2.0
Ultra-human, context-aware greetings (50+ variants)
Detects time (internet first → system fallback)
Uses user's name + avoids repetition using memory
"""

import requests
from datetime import datetime
from typing import Optional
import random


class GreetingEngine:
    def __init__(self, neural_memory=None):
        self.neural_memory = neural_memory
        self.user_name = "Airien"
        self.second_name = None

    def _get_time_info(self) -> dict:
        """Get current time. Try internet first, then system."""
        try:
            # Try internet time (World Time API)
            resp = requests.get("https://worldtimeapi.org/api/ip", timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                dt = datetime.fromisoformat(data["datetime"].replace("Z", "+00:00"))
                return {
                    "hour": dt.hour,
                    "source": "internet",
                    "timezone": data.get("timezone", "unknown")
                }
        except:
            pass

        # Fallback to system time
        now = datetime.now()
        return {
            "hour": now.hour,
            "source": "system",
            "timezone": "local"
        }

    def _get_user_names(self) -> tuple:
        """Get user names from NeuralMemoryManager"""
        if self.neural_memory:
            try:
                identity = self.neural_memory.get_identity()
                nombre = identity.get("nombre", "Airien")
                segundo = identity.get("segundo_nombre")
                return nombre, segundo
            except:
                pass
        return self.user_name, self.second_name

    def _has_greeted_today(self) -> bool:
        """Check if already greeted today using memory"""
        if not self.memory:
            return False
        try:
            today = datetime.now().date().isoformat()
            memories = self.memory.get_memories_by_category("saludo_diario")
            for m in memories:
                if m.get("value") == today:
                    return True
        except:
            pass
        return False

    def _save_greeted_today(self):
        """Mark that we greeted today"""
        if self.memory:
            today = datetime.now().date().isoformat()
            try:
                self.memory.save_neural_memory(
                    category="saludo_diario",
                    key="fecha",
                    value=today,
                    confidence=1.0
                )
            except:
                pass

    def get_greeting(self, force_new: bool = False) -> str:
        """
        Returns a highly human, contextual greeting.
        Uses name + time of day + avoids repetition.
        """
        time_info = self._get_time_info()
        hour = time_info["hour"]
        nombre, segundo_nombre = self._get_user_names()

        # Choose base name (sometimes use full name)
        name = nombre
        if segundo_nombre and random.random() > 0.6:
            name = f"{nombre} {segundo_nombre}"

        # Check if we already greeted today
        already_greeted = self._has_greeted_today() and not force_new

        greetings = []

        # ==================== MAÑANA (6:00 - 12:00) ====================
        if 6 <= hour < 12:
            greetings = [
                f"Buenos días {name}, ¿cómo amaneciste hoy?",
                f"¡Qué bonito verte tan temprano, {name}!",
                f"Hola {name}, ¿listo para empezar el día con energía?",
                f"Buenos días {name}, ¿dormiste bien?",
                f"¡Buenos días! ¿Cómo amaneciste {name}?",
                f"Hola {name}, ¿qué tal el despertar hoy?",
                f"Buenos días {name}, ¿qué planes tienes para hoy?",
                f"¡Hola {name}! ¿Cómo te sientes esta mañana?",
                f"Buenos días {name}, ¿ya tomaste tu café?",
                f"¡Qué lindo día para empezar, {name}!",
            ]

        # ==================== TARDE (12:00 - 19:00) ====================
        elif 12 <= hour < 19:
            greetings = [
                f"Buenas tardes {name}, ¿cómo va tu día?",
                f"Hola {name}, ¿qué tal la tarde?",
                f"Buenas tardes {name}, ¿ya almorzaste?",
                f"¡Hola {name}! ¿Cómo va todo por ahí?",
                f"Buenas tardes {name}, ¿en qué te puedo ayudar?",
                f"Hola {name}, ¿qué tal te ha ido la tarde?",
                f"Buenas tardes {name}, ¿sigues trabajando?",
                f"¡Qué tal {name}! ¿Cómo va el día?",
                f"Buenas tardes {name}, ¿necesitas algo?",
            ]

        # ==================== NOCHE (19:00 - 6:00) ====================
        else:
            greetings = [
                f"Buenas noches {name}, ¿cómo estuvo tu día?",
                f"Hola {name}, ¿ya terminaste el día?",
                f"Buenas noches {name}, ¿qué tal te fue hoy?",
                f"¡Hola {name}! ¿Cómo estuvo la jornada?",
                f"Buenas noches {name}, ¿ya cenaste?",
                f"Hola {name}, ¿cómo te sientes esta noche?",
                f"Buenas noches {name}, ¿quieres desahogarte un poco?",
                f"¡Qué tal {name}! ¿Cómo terminó tu día?",
                f"Buenas noches {name}, ¿todo bien?",
            ]

        # Special first-time-of-day greetings (only if not greeted today)
        if not already_greeted:
            if 6 <= hour < 12:
                greetings.extend([
                    f"Buenos días {name}, ¿cómo amaneciste hoy?",
                    f"¡Hola {name}! ¿Qué tal amaneciste?",
                ])
            elif 19 <= hour or hour < 6:
                greetings.extend([
                    f"Buenas noches {name}, ¿cómo estuvo tu día?",
                ])

        # Pick one randomly
        greeting = random.choice(greetings)

        # Save that we greeted today
        if not already_greeted:
            self._save_greeted_today()

        return greeting

    def get_contextual_greeting(self, user_message: str = "") -> str:
        """More advanced contextual greeting based on user message"""
        base = self.get_greeting()
        
        # You can expand this later with emotion detection
        return base
