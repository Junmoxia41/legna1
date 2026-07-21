try:
    import pyautogui
except ImportError:
    pyautogui = None
from tools.base import Tool

class ScreenshotTool(Tool):
    def __init__(self):
        super().__init__(name="take_screenshot", description="Captura la pantalla y la guarda")

    def execute(self, path="screenshot.png"):
        if not pyautogui: return "Error: pyautogui no instalado."
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(path)
            return f"Captura guardada en: {path}"
        except Exception as e:
            return f"Error en screenshot: {str(e)}"

class LocateOnScreenTool(Tool):
    def __init__(self):
        super().__init__(name="locate_image", description="Busca una imagen en la pantalla")

    def execute(self, image_path, confidence=0.9):
        if not pyautogui: return "Error: pyautogui no instalado."
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                return {"x": location.left, "y": location.top, "width": location.width, "height": location.height}
            return "No se encontró la imagen en pantalla."
        except Exception as e:
            return f"Error en locate_image: {str(e)}"
