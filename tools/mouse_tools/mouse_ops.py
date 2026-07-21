try:
    import pyautogui
except ImportError:
    pyautogui = None
from tools.base import Tool

class MouseClickTool(Tool):
    def __init__(self):
        super().__init__(name="mouse_click", description="Hace clic en una posición (x, y)")

    def execute(self, x, y, button='left', clicks=1):
        if not pyautogui: return "Error: pyautogui no instalado."
        try:
            pyautogui.click(x=x, y=y, button=button, clicks=clicks)
            return f"Clic {button} en ({x}, {y}) realizado {clicks} veces."
        except Exception as e:
            return f"Error en mouse_click: {str(e)}"

class MouseMoveTool(Tool):
    def __init__(self):
        super().__init__(name="mouse_move", description="Mueve el cursor a (x, y)")

    def execute(self, x, y, duration=0.1):
        if not pyautogui: return "Error: pyautogui no instalado."
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return f"Cursor movido a ({x}, {y})."
        except Exception as e:
            return f"Error en mouse_move: {str(e)}"

class ScreenSizeTool(Tool):
    def __init__(self):
        super().__init__(name="screen_size", description="Obtiene el tamaño de la pantalla")

    def execute(self):
        if not pyautogui: return "Error: pyautogui no instalado."
        return pyautogui.size()
