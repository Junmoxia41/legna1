import os
from tools.base import Tool

class CreateFileTool(Tool):
    def __init__(self):
        super().__init__(name="create_file", description="Crea un archivo nuevo")

    def execute(self, path, content=""):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Archivo creado con éxito en: {path}"
        except Exception as e:
            return f"Error al crear archivo: {str(e)}"

class WriteFileTool(Tool):
    def __init__(self):
        super().__init__(name="write_file", description="Escribe contenido en un archivo existente")

    def execute(self, path, content, mode='a'):
        try:
            with open(path, mode, encoding='utf-8') as f:
                f.write(content)
            return f"Contenido escrito en: {path}"
        except Exception as e:
            return f"Error al escribir en archivo: {str(e)}"

class ReadFileTool(Tool):
    def __init__(self):
        super().__init__(name="read_file", description="Lee el contenido de un archivo")

    def execute(self, path):
        try:
            if not os.path.exists(path):
                return "El archivo no existe."
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error al leer archivo: {str(e)}"
