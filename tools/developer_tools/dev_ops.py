import subprocess
from tools.base import Tool

class TestRunnerTool(Tool):
    def __init__(self):
        super().__init__(name="run_tests", description="Ejecuta pruebas (pytest) en un directorio")

    def execute(self, path="."):
        try:
            result = subprocess.run(f"pytest {path}", shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return str(e)

class CompileTool(Tool):
    def __init__(self):
        super().__init__(name="compile_code", description="Compila archivos (gcc, node, etc.)")

    def execute(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return str(e)
