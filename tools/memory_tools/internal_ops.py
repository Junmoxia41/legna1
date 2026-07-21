from tools.base import Tool

class MemorySearchTool(Tool):
    def __init__(self, memory_manager):
        super().__init__(name="memory_search", description="Busca en la memoria consolidada de Legna")
        self.mm = memory_manager

    def execute(self, query=None):
        try:
            memories = self.mm.load_memories()
            if query:
                return [m for m in memories if query.lower() in str(m).lower()]
            return memories
        except Exception as e:
            return str(e)

class ObservationSearchTool(Tool):
    def __init__(self, memory_manager):
        super().__init__(name="observation_search", description="Busca en las observaciones recientes (corto plazo)")
        self.mm = memory_manager

    def execute(self):
        try:
            return self.mm.load_observations()
        except Exception as e:
            return str(e)
