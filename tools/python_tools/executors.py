import subprocess
import os
from tools.base import Tool

class PipInstallTool(Tool):
    def __init__(self):
        super().__init__(name="pip_install", description="Instala librerías de Python")

    def execute(self, package):
        try:
            result = subprocess.run(f"pip install {package}", shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return str(e)

class PythonScriptTool(Tool):
    def __init__(self):
        super().__init__(name="run_python", description="Ejecuta un script de Python")

    def execute(self, path):
        try:
            result = subprocess.run(f"python3 {path}", shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return str(e)
