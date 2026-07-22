"""Explicit user terminal sessions restricted to an opened workspace."""
import os
import subprocess
from pathlib import Path
from uuid import uuid4

from ide.policy import WorkspacePolicy


class TerminalService:
    MAX_OUTPUT = 180_000
    TIMEOUT_SECONDS = 45

    def __init__(self, policy: WorkspacePolicy):
        self.policy = policy
        self.sessions = {}

    def create(self, label=None, relative_cwd=""):
        cwd = self.policy.resolve(relative_cwd)
        if not cwd.is_dir():
            raise ValueError("El directorio de terminal no existe.")
        session_id = uuid4().hex
        session = {"id": session_id, "label": label or f"Terminal {len(self.sessions)+1}", "cwd": self._relative(cwd), "history": []}
        self.sessions[session_id] = session
        return self._summary(session)

    def list(self):
        return [self._summary(session) for session in self.sessions.values()]

    def close(self, session_id):
        if session_id not in self.sessions:
            raise ValueError("Sesión de terminal no encontrada.")
        del self.sessions[session_id]
        return True

    def run(self, session_id, command):
        session = self.sessions.get(session_id)
        command = (command or "").strip()
        if not session:
            raise ValueError("Sesión de terminal no encontrada.")
        if not command:
            raise ValueError("El comando está vacío.")
        cwd = self.policy.resolve(session["cwd"])
        # A terminal intentionally supports shell syntax, but shell=True is never used.
        invocation = ["cmd.exe", "/d", "/c", command] if os.name == "nt" else ["bash", "-lc", command]
        try:
            result = subprocess.run(invocation, cwd=cwd, capture_output=True, text=True,
                                    timeout=self.TIMEOUT_SECONDS, encoding="utf-8", errors="replace")
            output = (result.stdout or "") + (result.stderr or "")
            payload = {"command": command, "output": output[-self.MAX_OUTPUT:], "returncode": result.returncode, "timed_out": False}
        except subprocess.TimeoutExpired as error:
            output = ((error.stdout or "") + (error.stderr or ""))[-self.MAX_OUTPUT:]
            payload = {"command": command, "output": output, "returncode": None, "timed_out": True}
        session["history"].append(payload)
        session["history"] = session["history"][-100:]
        return payload

    def _summary(self, session):
        return {"id": session["id"], "label": session["label"], "cwd": session["cwd"], "history": session["history"]}

    def _relative(self, path: Path):
        return path.relative_to(self.policy.root).as_posix()
