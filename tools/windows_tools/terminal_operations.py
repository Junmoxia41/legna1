import subprocess
from tools.base import Tool

class ExecuteCommandTool(Tool):
    def __init__(self):
        super().__init__(name="execute_cmd", description="Ejecuta un comando en CMD o PowerShell")

    def execute(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error ({result.returncode}): {result.stderr}"
        except Exception as e:
            return f"Error de ejecución: {str(e)}"
