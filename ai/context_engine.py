"""
Context Engine - Legna v2.0
Loads and injects neural memory context into conversations
Makes Legna feel like she truly remembers everything
"""

from memory.neural_memory import NeuralMemoryManager


class ContextEngine:
    def __init__(self, neural_memory: NeuralMemoryManager = None):
        self.neural_memory = neural_memory or NeuralMemoryManager()

    def get_identity_context(self) -> str:
        """Returns a natural language summary of user identity"""
        identity = self.neural_memory.get_identity()
        
        parts = []
        if identity.get("nombre"):
            parts.append(f"Te llamas {identity['nombre']}")
        if identity.get("segundo_nombre"):
            parts.append(f"tu segundo nombre es {identity['segundo_nombre']}")
        if identity.get("edad"):
            parts.append(f"tienes {identity['edad']} años")

        if parts:
            return "Recuerdo que " + ", ".join(parts) + "."
        return ""

    def get_recent_commands(self, limit: int = 3) -> list:
        """Returns recently learned commands"""
        commands = self.neural_memory.get_memories_by_category("comando")
        return [c["key"] for c in commands[-limit:]]

    def get_project_context(self) -> str:
        """Returns info about known projects"""
        projects = self.neural_memory.get_memories_by_category("proyecto")
        if projects:
            names = [p["value"] for p in projects[:2]]
            return f"Estamos trabajando en los proyectos: {', '.join(names)}."
        return ""

    def build_chat_context(self) -> str:
        """Builds a rich context string to inject into responses"""
        identity = self.get_identity_context()
        projects = self.get_project_context()
        commands = self.get_recent_commands()

        context_parts = []
        if identity:
            context_parts.append(identity)
        if projects:
            context_parts.append(projects)
        if commands:
            context_parts.append(f"Recuerdo los comandos: {', '.join(commands)}.")

        return " ".join(context_parts)

    def get_memory_summary(self) -> dict:
        """Returns structured summary for UI"""
        return {
            "identity": self.neural_memory.get_identity(),
            "commands": self.get_recent_commands(5),
            "projects": [m["value"] for m in self.neural_memory.get_memories_by_category("proyecto")]
        }
