"""Workspace-scoped Git service. Mutations are explicit and never use shell strings."""
import subprocess
from ide.policy import WorkspacePolicy


class GitService:
    def __init__(self, policy: WorkspacePolicy): self.policy = policy

    def status(self):
        if not self._available(): return {"available": False, "branch": None, "changes": [], "ahead": 0, "behind": 0}
        branch_line = self._run(["git", "status", "--porcelain=v1", "-b"]).splitlines()
        header = branch_line[0] if branch_line else ""
        branch = self._run(["git", "branch", "--show-current"]).strip() or "DETACHED"
        changes = []
        for line in branch_line[1:]:
            if len(line) < 4: continue
            changes.append({"index": line[0], "worktree": line[1], "path": line[3:], "staged": line[0] != " ", "unstaged": line[1] != " "})
        ahead, behind = self._ahead_behind()
        return {"available": True, "branch": branch, "changes": changes, "ahead": ahead, "behind": behind, "header": header}

    def diff(self, relative_path=None, staged=False):
        if not self._available(): return {"available": False, "diff": ""}
        command = ["git", "diff"] + (["--cached"] if staged else []) + ["--"] + ([relative_path] if relative_path else [])
        return {"available": True, "diff": self._run(command)}

    def stage(self, paths):
        self._require_repo(); values = self._paths(paths)
        self._run(["git", "add", "--", *values]); return self.status()

    def unstage(self, paths):
        self._require_repo(); values = self._paths(paths)
        self._run(["git", "reset", "HEAD", "--", *values]); return self.status()

    def commit(self, message):
        self._require_repo()
        message = (message or "").strip()
        if not message: raise ValueError("El mensaje de commit es obligatorio.")
        output = self._run(["git", "commit", "-m", message])
        return {"output": output, "status": self.status()}

    def branches(self):
        if not self._available(): return {"available": False, "branches": []}
        lines = self._run(["git", "branch", "--format=%(HEAD)|%(refname:short)"]).splitlines()
        return {"available": True, "branches": [{"name": line.split("|", 1)[1], "current": line.startswith("*")} for line in lines if "|" in line]}

    def _available(self):
        try: return self._run(["git", "rev-parse", "--is-inside-work-tree"]).strip() == "true"
        except (FileNotFoundError, subprocess.CalledProcessError): return False

    def _require_repo(self):
        if not self._available(): raise ValueError("Este workspace no es un repositorio Git.")

    def _paths(self, paths):
        values = [str(value) for value in (paths if isinstance(paths, list) else [paths]) if value]
        if not values: raise ValueError("Selecciona al menos un archivo.")
        for value in values: self.policy.resolve(value)
        return values

    def _ahead_behind(self):
        try:
            value = self._run(["git", "rev-list", "--left-right", "--count", "@{upstream}...HEAD"]).strip().split()
            return int(value[1]), int(value[0])
        except subprocess.CalledProcessError: return 0, 0

    def _run(self, command):
        result = subprocess.run(command, cwd=self.policy.root, capture_output=True, text=True, timeout=20, encoding="utf-8", errors="replace")
        if result.returncode: raise subprocess.CalledProcessError(result.returncode, command, result.stdout, result.stderr)
        return result.stdout
