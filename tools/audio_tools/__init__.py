from tools.base import ToolCategory

class AudioToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="AudioTools", description="Herramientas de Audio (Requiere PyAudio)")
        # No registramos herramientas si falla la dependencia
        self.status = "Inactivo (Falta PyAudio)"

    def list_tools(self):
        return {"Estado": self.status}
