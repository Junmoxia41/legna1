from tools.base import ToolCategory
from tools.database_tools.sqlite_ops import SQLiteQueryTool

class DatabaseToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="DatabaseTools", description="Herramientas para gestión de bases de datos")
        self.register_tool(SQLiteQueryTool())
