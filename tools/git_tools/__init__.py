from tools.base import ToolCategory
from tools.git_tools.git_ops import GitCloneTool, GitCommitTool, GitPushTool

class GitToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="GitTools", description="Operaciones básicas de Git")
        self.register_tool(GitCloneTool())
        self.register_tool(GitCommitTool())
        self.register_tool(GitPushTool())
