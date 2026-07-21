from tools.base import ToolCategory
from tools.memory_tools.internal_ops import MemorySearchTool, ObservationSearchTool

class MemoryToolsCategory(ToolCategory):
    def __init__(self, memory_manager):
        super().__init__(name="MemoryTools", description="Herramientas de acceso al sistema de memoria de Legna")
        self.register_tool(MemorySearchTool(memory_manager))
        self.register_tool(ObservationSearchTool(memory_manager))
