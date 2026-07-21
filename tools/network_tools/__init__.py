from tools.base import ToolCategory
from tools.network_tools.requests_ops import HTTPRequestTool, DownloadFileTool

class NetworkToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="NetworkTools", description="Herramientas de red y peticiones HTTP")
        self.register_tool(HTTPRequestTool())
        self.register_tool(DownloadFileTool())
