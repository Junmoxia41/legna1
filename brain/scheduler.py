"""Task planning and activity history for Legna's specialist agents."""
from datetime import datetime
from typing import Dict, List
from agents.registry import AgentRegistry


class AgentScheduler:
    def __init__(self, agents: AgentRegistry):
        self.agents = agents
        self._history: List[Dict] = []

    def start(self, classification: Dict, message: str) -> Dict:
        selected = classification["agents"]
        for agent_id in selected:
            self.agents.set_state(agent_id, "thinking" if agent_id == "core" else "waiting")
        task = {
            "id": f"task_{int(datetime.now().timestamp() * 1000)}",
            "created_at": datetime.now().isoformat(),
            "status": "running",
            "agents": selected,
            "intent": classification["primary"],
            "summary": message[:120],
        }
        self._history.insert(0, task)
        self._history = self._history[:30]
        return task

    def finish(self, task: Dict, success: bool = True):
        task["status"] = "completed" if success else "error"
        task["completed_at"] = datetime.now().isoformat()
        for agent_id in task["agents"]:
            self.agents.set_state(agent_id, "idle" if success else "error")

    def recent(self, limit: int = 8) -> List[Dict]:
        return self._history[:limit]
