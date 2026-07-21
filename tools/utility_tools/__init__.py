from tools.base import ToolCategory
from tools.utility_tools.utils import TimeTool, EchoTool

class UtilityToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="UtilityTools", description="Utilidades generales del sistema")
        self.register_tool(TimeTool())
        self.register_tool(EchoTool())
