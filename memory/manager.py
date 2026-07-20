from memory.database import Database
from memory.knowledge_engine import KnowledgeEngine
from memory.short_term_memory import ShortTermMemory


class MemoryManager:

    def __init__(self):

        print("Memory Manager iniciado.")

        self.database = Database()
        self.database.initialize()

        self.knowledge_engine = KnowledgeEngine()

        self.short_term_memory = ShortTermMemory(
            self.database
        )

    # =====================================================
    # MEMORY
    # =====================================================

    def save_memory(self, memory):

        self.database.save_memory(memory)

    def load_memories(self):

        return self.database.load_memories()

    # =====================================================
    # KNOWLEDGE
    # =====================================================

    def extract_knowledge(self, message):

        evaluations = self.knowledge_engine.extract(message)

        self.short_term_memory.record(
            evaluations
        )

        return evaluations

    # =====================================================
    # SHORT TERM MEMORY
    # =====================================================

    def load_observations(self):

        return self.short_term_memory.load()