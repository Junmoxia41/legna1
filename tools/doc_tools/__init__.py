from tools.base import ToolCategory
from tools.doc_tools.handlers import JSONTool, MarkdownTool

class DocToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="DocTools", description="Herramientas para manejo de documentos (PDF, Word, Excel, JSON, etc.)")
        self.register_tool(JSONTool())
        self.register_tool(MarkdownTool())
