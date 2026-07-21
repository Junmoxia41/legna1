from tools.base import ToolCategory
from tools.vision_tools.image_ops import ScreenshotTool, LocateOnScreenTool

class VisionToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="VisionTools", description="Herramientas de visión y análisis de pantalla")
        self.register_tool(ScreenshotTool())
        self.register_tool(LocateOnScreenTool())
