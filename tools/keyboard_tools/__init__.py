from tools.base import ToolCategory
from tools.keyboard_tools.keyboard_ops import TypeTextTool, HotkeyTool, PressKeyTool

class KeyboardToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="KeyboardTools", description="Simulación de teclado y atajos")
        self.register_tool(TypeTextTool())
        self.register_tool(HotkeyTool())
        self.register_tool(PressKeyTool())
