import logging
from tools.base import ToolCategory, Tool

class ToolRegistry:
    """
    Registro centralizado de todas las categorías y herramientas de Legna.
    """
    def __init__(self):
        self.categories = {}
        self.logger = logging.getLogger(__name__)

    def register_category(self, category: ToolCategory):
        self.categories[category.name] = category
        self.logger.info(f"Categoría de herramientas registrada: {category.name}")

    def get_category(self, name: str) -> ToolCategory:
        return self.categories.get(name)

    def find_tool(self, tool_name: str) -> Tool:
        """
        Busca una herramienta en todas las categorías registradas.
        """
        for category in self.categories.values():
            tool = category.get_tool(tool_name)
            if tool:
                return tool
        return None

    def execute_tool(self, tool_name: str, **kwargs):
        tool = self.find_tool(tool_name)
        if tool:
            return tool.execute(**kwargs)
        return f"Herramienta '{tool_name}' no encontrada."

    def list_all_tools(self):
        summary = {}
        for cat_name, category in self.categories.items():
            summary[cat_name] = category.list_tools()
        return summary
