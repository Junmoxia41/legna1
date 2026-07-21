from tools.base import ToolCategory
from tools.mouse_tools.mouse_ops import MouseClickTool, MouseMoveTool, ScreenSizeTool

class MouseToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="MouseTools", description="Control del cursor y clics del ratón")
        self.register_tool(MouseClickTool())
        self.register_tool(MouseMoveTool())
        self.register_tool(ScreenSizeTool())
