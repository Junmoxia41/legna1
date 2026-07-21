from tools.base import ToolCategory
from tools.github_tools.api_ops import GithubAPITool

class GithubToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="GithubTools", description="Integración con la API de GitHub")
        self.register_tool(GithubAPITool())
