from abc import ABC, abstractmethod

class Tool(ABC):
    """
    Clase base para una herramienta individual.
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, **kwargs):
        pass

class ToolCategory(ABC):
    """
    Clase base para una categoría que agrupa múltiples herramientas.
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.tools = {}

    def register_tool(self, tool: Tool):
        self.tools[tool.name] = tool

    def get_tool(self, name: str) -> Tool:
        return self.tools.get(name)

    def list_tools(self):
        return {name: tool.description for name, tool in self.tools.items()}
