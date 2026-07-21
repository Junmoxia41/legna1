from memory.database import Database
from memory.knowledge_engine import KnowledgeEngine
from memory.short_term_memory import ShortTermMemory
from commands.manager import CommandManager
from commands.open_command import OpenCommand
from tools.registry import ToolRegistry
from tools.file_tools import FileToolsCategory
from tools.windows_tools import WindowsToolsCategory
from tools.doc_tools import DocToolsCategory
from tools.python_tools import PythonToolsCategory
from tools.mouse_tools import MouseToolsCategory
from tools.keyboard_tools import KeyboardToolsCategory
from tools.vision_tools import VisionToolsCategory
from tools.git_tools import GitToolsCategory
from tools.network_tools import NetworkToolsCategory
from tools.browser_tools import BrowserToolsCategory
from tools.github_tools import GithubToolsCategory
from tools.developer_tools import DeveloperToolsCategory
from tools.database_tools import DatabaseToolsCategory
from tools.memory_tools import MemoryToolsCategory
from tools.ai_provider_tools import AIProviderToolsCategory
from tools.automation_tools import AutomationToolsCategory
from tools.utility_tools import UtilityToolsCategory
from tools.skeletons import AudioToolsCategory


class MemoryManager:

    def __init__(self):

        print("Memory Manager iniciado.")

        self.database = Database()
        self.database.initialize()

        self.knowledge_engine = KnowledgeEngine()

        self.short_term_memory = ShortTermMemory(
            self.database
        )
        
        # Registro de Herramientas Modular
        self.tool_registry = ToolRegistry()
        self._initialize_tools()
        
        # Sistema de comandos integrado
        self.command_manager = CommandManager()
        self._register_default_commands()

    def _initialize_tools(self):
        # Registro de todas las categorías del catálogo
        self.tool_registry.register_category(FileToolsCategory())
        self.tool_registry.register_category(WindowsToolsCategory())
        self.tool_registry.register_category(DocToolsCategory())
        self.tool_registry.register_category(PythonToolsCategory())
        self.tool_registry.register_category(VisionToolsCategory())
        self.tool_registry.register_category(MouseToolsCategory())
        self.tool_registry.register_category(KeyboardToolsCategory())
        self.tool_registry.register_category(GitToolsCategory())
        self.tool_registry.register_category(NetworkToolsCategory())
        self.tool_registry.register_category(BrowserToolsCategory())
        self.tool_registry.register_category(GithubToolsCategory())
        self.tool_registry.register_category(DeveloperToolsCategory())
        self.tool_registry.register_category(DatabaseToolsCategory())
        self.tool_registry.register_category(MemoryToolsCategory(self))
        self.tool_registry.register_category(AIProviderToolsCategory())
        self.tool_registry.register_category(AutomationToolsCategory(self.tool_registry))
        self.tool_registry.register_category(UtilityToolsCategory())
        
        # Skeletons para el resto (Audio pendiente de drivers específicos)
        self.tool_registry.register_category(AudioToolsCategory())

    def _register_default_commands(self):
        self.command_manager.register_command(OpenCommand())

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
        
        # Filtro para reconocer y ejecutar comandos
        for eval in evaluations:
            if eval.memory_type == "command":
                trigger = eval.canonical_key.split(":")[-1]
                params = eval.content
                result = self.command_manager.execute_command(trigger, params)
                print(f"[Command System] {result}")

        return evaluations

    # =====================================================
    # SHORT TERM MEMORY
    # =====================================================

    def load_observations(self):

        return self.short_term_memory.load()