import psutil
import platform
from tools.base import Tool

class ProcessTool(Tool):
    def __init__(self):
        super().__init__(name="list_processes", description="Lista los procesos activos en el sistema")

    def execute(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            processes.append(proc.info)
        return processes[:20] # Limitamos a los primeros 20 por brevedad

class SystemInfoTool(Tool):
    def __init__(self):
        super().__init__(name="system_info", description="Obtiene información del hardware y SO")

    def execute(self):
        info = {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(),
            "memory": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"
        }
        return info
