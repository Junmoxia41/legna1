from tools.base import ToolCategory
from tools.python_tools.executors import PipInstallTool, PythonScriptTool

class PythonToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="PythonTools", description="Herramientas para desarrollo y ejecución en Python")
        self.register_tool(PipInstallTool())
        self.register_tool(PythonScriptTool())
