import datetime
from tools.base import Tool

class TimeTool(Tool):
    def __init__(self):
        super().__init__(name="get_time", description="Obtiene la fecha y hora actual")

    def execute(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class EchoTool(Tool):
    def __init__(self):
        super().__init__(name="echo", description="Devuelve el mismo mensaje (para debug)")

    def execute(self, message):
        return message
