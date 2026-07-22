"""Small, serializable contracts used by Legna IDE services."""
from dataclasses import asdict, dataclass
from typing import Optional

@dataclass(frozen=True)
class WorkspaceRef:
    id: str
    name: str
    root: str

    def to_dict(self): return asdict(self)

@dataclass(frozen=True)
class FileEntry:
    path: str
    name: str
    kind: str
    has_children: bool = False
    size: Optional[int] = None

    def to_dict(self): return asdict(self)
