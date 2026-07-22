"""Safe document persistence and change detection for Monaco documents."""
import hashlib
from pathlib import Path
from ide.policy import WorkspacePolicy

class DocumentService:
    def __init__(self, policy: WorkspacePolicy): self.policy = policy

    @staticmethod
    def _hash(content: str): return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def read(self, relative_path):
        path = self.policy.resolve(relative_path)
        if not path.is_file(): raise FileNotFoundError('El documento no existe.')
        if path.stat().st_size > self.policy.MAX_DOCUMENT_BYTES: raise ValueError('El documento supera el límite de lectura del IDE.')
        content = path.read_text(encoding='utf-8', errors='replace')
        return {'path': relative_path, 'content': content, 'version': self._hash(content), 'modified_at': path.stat().st_mtime}

    def save(self, relative_path, content, expected_version=None):
        if not isinstance(content, str): raise ValueError('El contenido debe ser texto.')
        path = self.policy.resolve(relative_path)
        if path.exists() and expected_version:
            current = path.read_text(encoding='utf-8', errors='replace')
            if self._hash(current) != expected_version: raise RuntimeError('El archivo cambió en disco. Recarga antes de guardar.')
        path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content, encoding='utf-8')
        return self.read(relative_path)
