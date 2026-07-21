from tools.base import ToolCategory
from tools.ai_provider_tools.adapters import OpenAIAdapterTool, AnthropicAdapterTool

class AIProviderToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="AIProviderTools", description="Adaptadores para diferentes proveedores de IA")
        self.register_tool(OpenAIAdapterTool())
        self.register_tool(AnthropicAdapterTool())
