from tools.base import ToolCategory
from tools.automation_tools.workflow_ops import TaskTimerTool, SimpleWorkflowTool

class AutomationToolsCategory(ToolCategory):
    def __init__(self, tool_registry):
        super().__init__(name="AutomationTools", description="Herramientas para flujos de trabajo y automatización")
        self.register_tool(TaskTimerTool())
        self.register_tool(SimpleWorkflowTool(tool_registry))
