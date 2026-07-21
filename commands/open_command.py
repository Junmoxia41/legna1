from commands.base import Command

class OpenCommand(Command):
    def __init__(self):
        super().__init__(name="abre", description="Abre una aplicación o recurso")
        self.aliases = ["ejecuta"]

    def execute(self, params):
        return f"Ejecutando acción de apertura para: {params}"
