"""
Neural Memory Manager - Legna v2.0
Handles categorized neural memories (nombre, segundo_nombre, edad, comandos, etc.)
"""

import json
from datetime import datetime
from pathlib import Path


class NeuralMemoryManager:
    def __init__(self, db_path="/home/user/legna1/database/neural_memory.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.memories = self._load()

    def _load(self):
        if self.db_path.exists():
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {"memories": []}
        return {"memories": []}

    def _save(self):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.memories, f, indent=2, ensure_ascii=False)

    def save_memory(self, category: str, key: str, value: str, confidence: float = 0.9, notes: str = ""):
        """Save or update a neural memory"""
        memory = {
            "id": str(datetime.now().timestamp()),
            "category": category.lower(),
            "key": key.lower(),
            "value": value,
            "confidence": round(confidence, 2),
            "timestamp": datetime.now().isoformat(),
            "notes": notes
        }

        # Update if exists (same category + key)
        updated = False
        for i, m in enumerate(self.memories["memories"]):
            if m["category"] == category.lower() and m["key"] == key.lower():
                self.memories["memories"][i] = memory
                updated = True
                break

        if not updated:
            self.memories["memories"].append(memory)

        self._save()
        return memory

    def get_memories_by_category(self, category: str):
        return [m for m in self.memories["memories"] if m["category"] == category.lower()]

    def get_all_memories(self):
        return self.memories["memories"]

    def get_identity(self):
        """Quick access to user identity"""
        nombre = None
        segundo = None
        edad = None

        for m in self.memories["memories"]:
            if m["category"] == "nombre" and m["key"] == "nombre":
                nombre = m["value"]
            if m["category"] == "nombre" and m["key"] == "segundo_nombre":
                segundo = m["value"]
            if m["category"] == "edad":
                edad = m["value"]

        return {
            "nombre": nombre or "Airien",
            "segundo_nombre": segundo,
            "edad": edad
        }

    def search_memories(self, query: str):
        query = query.lower()
        return [m for m in self.memories["memories"] 
                if query in m["key"] or query in m["value"] or query in m["category"]]
