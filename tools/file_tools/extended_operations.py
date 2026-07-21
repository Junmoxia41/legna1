import os
import shutil
import glob
from tools.base import Tool

class MoveFileTool(Tool):
    def __init__(self):
        super().__init__(name="move_file", description="Mueve o renombra un archivo o carpeta")

    def execute(self, src, dst):
        try:
            shutil.move(src, dst)
            return f"Movido de {src} a {dst}"
        except Exception as e:
            return f"Error al mover: {str(e)}"

class DeleteFileTool(Tool):
    def __init__(self):
        super().__init__(name="delete_file", description="Elimina un archivo o carpeta")

    def execute(self, path):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return f"Eliminado: {path}"
        except Exception as e:
            return f"Error al eliminar: {str(e)}"

class CreateFolderTool(Tool):
    def __init__(self):
        super().__init__(name="create_folder", description="Crea una carpeta nueva")

    def execute(self, path):
        try:
            os.makedirs(path, exist_ok=True)
            return f"Carpeta creada: {path}"
        except Exception as e:
            return f"Error al crear carpeta: {str(e)}"

class SearchFileTool(Tool):
    def __init__(self):
        super().__init__(name="search_file", description="Busca archivos usando un patrón (ej: *.txt)")

    def execute(self, pattern, root_dir="."):
        try:
            files = glob.glob(os.path.join(root_dir, pattern), recursive=True)
            return files if files else "No se encontraron archivos."
        except Exception as e:
            return f"Error en la búsqueda: {str(e)}"
