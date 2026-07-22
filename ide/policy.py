"""Workspace sandbox. All new IDE file operations pass through this policy."""
from pathlib import Path

class WorkspacePolicy:
    EXCLUDED_NAMES = {'.git', '.hg', '.svn', 'node_modules', '.venv', 'venv', '__pycache__', '.pytest_cache', '.legna-trash'}
    MAX_DOCUMENT_BYTES = 3 * 1024 * 1024

    def __init__(self, root): self.root = Path(root).resolve()

    def resolve(self, relative_path=''):
        candidate = (self.root / relative_path).resolve()
        if candidate != self.root and self.root not in candidate.parents:
            raise ValueError('La ruta está fuera del workspace autorizado.')
        return candidate

    def visible(self, path: Path) -> bool:
        return not any(part in self.EXCLUDED_NAMES for part in path.parts)
