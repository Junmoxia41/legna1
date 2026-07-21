from tools.base import ToolCategory
from tools.file_tools.file_operations import CreateFileTool, WriteFileTool, ReadFileTool
from tools.file_tools.extended_operations import MoveFileTool, DeleteFileTool, CreateFolderTool, SearchFileTool

class FileToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="FileTools", description="Herramientas para gestión de archivos y carpetas")
        self.register_tool(CreateFileTool())
        self.register_tool(WriteFileTool())
        self.register_tool(ReadFileTool())
        self.register_tool(MoveFileTool())
        self.register_tool(DeleteFileTool())
        self.register_tool(CreateFolderTool())
        self.register_tool(SearchFileTool())
