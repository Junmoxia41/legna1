"""Non-executing diagnostics providers. Python is the first built-in provider."""
from pathlib import Path
from ide.policy import WorkspacePolicy


class DiagnosticsService:
    MAX_WORKSPACE_FILES = 500

    def __init__(self, policy: WorkspacePolicy): self.policy = policy

    def analyze(self, relative_path):
        path = self.policy.resolve(relative_path)
        if path.suffix.lower() != ".py" or not path.is_file(): return []
        source = path.read_text(encoding="utf-8", errors="replace")
        diagnostics = self._syntax(relative_path, source)
        diagnostics.extend(self._style(relative_path, source))
        return sorted(diagnostics, key=lambda entry: (entry["line"], entry["column"], entry["severity"]))

    def analyze_workspace(self):
        diagnostics = []
        count = 0
        for path in self.policy.root.rglob("*.py"):
            if count >= self.MAX_WORKSPACE_FILES: break
            if not self.policy.visible(path): continue
            count += 1
            diagnostics.extend(self.analyze(path.relative_to(self.policy.root).as_posix()))
        return diagnostics

    @staticmethod
    def _syntax(relative_path, source):
        try:
            compile(source, relative_path, "exec")
            return []
        except SyntaxError as error:
            return [{"path": relative_path, "line": error.lineno or 1, "column": error.offset or 1,
                     "severity": "error", "code": "PY-SYNTAX", "message": error.msg, "source": "Python parser"}]

    @staticmethod
    def _style(relative_path, source):
        diagnostics = []
        for line_number, line in enumerate(source.splitlines(), 1):
            if line.rstrip() != line:
                diagnostics.append({"path": relative_path, "line": line_number, "column": len(line.rstrip())+1,
                                    "severity": "warning", "code": "STYLE-TRAILING", "message": "Espacio en blanco al final de línea.", "source": "Legna Quality"})
            if len(line) > 120:
                diagnostics.append({"path": relative_path, "line": line_number, "column": 121,
                                    "severity": "info", "code": "STYLE-LINE", "message": "Línea superior a 120 caracteres.", "source": "Legna Quality"})
            if "TODO" in line or "FIXME" in line:
                diagnostics.append({"path": relative_path, "line": line_number, "column": line.find("TODO") + 1 if "TODO" in line else line.find("FIXME") + 1,
                                    "severity": "hint", "code": "QUALITY-TODO", "message": "Pendiente detectado; considera crear una tarea o resolverlo.", "source": "Legna Quality"})
        return diagnostics
