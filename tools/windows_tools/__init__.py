from tools.base import ToolCategory
from tools.windows_tools.terminal_operations import ExecuteCommandTool
from tools.windows_tools.system_management import ProcessTool, SystemInfoTool

class WindowsToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="WindowsTools", description="Herramientas para interactuar con el sistema operativo Windows")
        self.register_tool(ExecuteCommandTool())
        self.register_tool(ProcessTool())
        self.register_tool(SystemInfoTool())
