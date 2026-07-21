import subprocess
from tools.base import Tool

class GitCloneTool(Tool):
    def __init__(self):
        super().__init__(name="git_clone", description="Clona un repositorio de Git")

    def execute(self, url, path="."):
        try:
            result = subprocess.run(f"git clone {url} {path}", shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return str(e)

class GitCommitTool(Tool):
    def __init__(self):
        super().__init__(name="git_commit", description="Realiza un add y commit en el repo")

    def execute(self, message):
        try:
            subprocess.run("git add .", shell=True)
            result = subprocess.run(f'git commit -m "{message}"', shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return str(e)

class GitPushTool(Tool):
    def __init__(self):
        super().__init__(name="git_push", description="Sube los cambios al remoto")

    def execute(self, remote="origin", branch="main"):
        try:
            result = subprocess.run(f"git push {remote} {branch}", shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return str(e)
