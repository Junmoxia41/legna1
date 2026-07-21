try:
    import pyautogui
except ImportError:
    pyautogui = None
from tools.base import Tool

class TypeTextTool(Tool):
    def __init__(self):
        super().__init__(name="keyboard_type", description="Escribe un texto")

    def execute(self, text, interval=0.1):
        if not pyautogui: return "Error: pyautogui no instalado."
        try:
            pyautogui.write(text, interval=interval)
            return f"Texto escrito: {text}"
        except Exception as e:
            return f"Error en keyboard_type: {str(e)}"

class HotkeyTool(Tool):
    def __init__(self):
        super().__init__(name="keyboard_hotkey", description="Presiona una combinación de teclas (ej: ctrl, c)")

    def execute(self, *args):
        if not pyautogui: return "Error: pyautogui no instalado."
        try:
            pyautogui.hotkey(*args)
            return f"Combinación ejecutada: {args}"
        except Exception as e:
            return f"Error en hotkey: {str(e)}"

class PressKeyTool(Tool):
    def __init__(self):
        super().__init__(name="keyboard_press", description="Presiona una tecla específica (ej: enter, esc)")

    def execute(self, key):
        if not pyautogui: return "Error: pyautogui no instalado."
        try:
            pyautogui.press(key)
            return f"Tecla presionada: {key}"
        except Exception as e:
            return f"Error en keyboard_press: {str(e)}"
