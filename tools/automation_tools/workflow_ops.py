import time
from tools.base import Tool

class TaskTimerTool(Tool):
    def __init__(self):
        super().__init__(name="wait", description="Espera una cantidad de segundos")

    def execute(self, seconds):
        time.sleep(float(seconds))
        return f"Espera de {seconds} segundos finalizada."

class SimpleWorkflowTool(Tool):
    def __init__(self, tool_registry):
        super().__init__(name="run_workflow", description="Ejecuta una lista de herramientas en secuencia")
        self.registry = tool_registry

    def execute(self, steps):
        """
        steps: Lista de dicts [{'tool': 'name', 'args': {}}]
        """
        results = []
        for step in steps:
            res = self.registry.execute_tool(step['tool'], **step['args'])
            results.append({step['tool']: res})
        return results
