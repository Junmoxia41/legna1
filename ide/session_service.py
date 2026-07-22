"""Persistent recoverable IDE session state, separate from UI components."""
import json
from pathlib import Path

class SessionService:
    def __init__(self, state_path):
        self.path = Path(state_path); self.path.parent.mkdir(parents=True, exist_ok=True)
    def load(self):
        try: return json.loads(self.path.read_text(encoding='utf-8'))
        except (OSError, ValueError): return {"workspaces": {}, "recent_workspaces": []}
    def save(self, state):
        self.path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')
        return state
