from tools.base import ToolCategory
from tools.browser_tools.browser_ops import OpenBrowserTool, SimpleScraperTool

class BrowserToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="BrowserTools", description="Herramientas para navegación y extracción web")
        self.register_tool(OpenBrowserTool())
        self.register_tool(SimpleScraperTool())
