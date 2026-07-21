from tools.base import ToolCategory
from tools.developer_tools.dev_ops import TestRunnerTool, CompileTool

class DeveloperToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="DeveloperTools", description="Herramientas para desarrollo, compilación y pruebas")
        self.register_tool(TestRunnerTool())
        self.register_tool(CompileTool())
