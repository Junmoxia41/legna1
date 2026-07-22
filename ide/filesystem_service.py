"""Lazy, sandboxed directory operations for the IDE explorer."""
import shutil
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from ide.models import FileEntry
from ide.policy import WorkspacePolicy


class FilesystemService:
    def __init__(self, policy: WorkspacePolicy):
        self.policy = policy

    def list_directory(self, relative_path=""):
        directory = self.policy.resolve(relative_path)
        if not directory.is_dir():
            raise ValueError("La ruta solicitada no es una carpeta.")
        entries = []
        for item in sorted(directory.iterdir(), key=lambda value: (not value.is_dir(), value.name.lower())):
            if not self.policy.visible(item):
                continue
            relative = item.relative_to(self.policy.root).as_posix()
            entries.append(FileEntry(
                relative, item.name, "directory" if item.is_dir() else "file",
                item.is_dir() and any(self.policy.visible(child) for child in item.iterdir()),
                None if item.is_dir() else item.stat().st_size,
            ).to_dict())
        return entries

    def create_file(self, relative_path, content=""):
        path = self.policy.resolve(relative_path)
        if path.exists():
            raise FileExistsError("Ya existe un elemento con ese nombre.")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return self._relative(path)

    def create_directory(self, relative_path):
        path = self.policy.resolve(relative_path)
        path.mkdir(parents=True, exist_ok=False)
        return self._relative(path)

    def rename(self, source, new_name):
        if not new_name or Path(new_name).name != new_name or new_name in {".", ".."}:
            raise ValueError("El nombre no es válido.")
        src = self._existing(source)
        destination = src.with_name(new_name)
        if destination.exists():
            raise FileExistsError("Ya existe un elemento con ese nombre.")
        src.rename(destination)
        return self._relative(destination)

    def move(self, source, destination):
        src, dst = self._existing(source), self.policy.resolve(destination)
        if dst.exists():
            raise FileExistsError("El destino ya existe.")
        if src.is_dir() and src in dst.parents:
            raise ValueError("No se puede mover una carpeta dentro de sí misma.")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        return self._relative(dst)

    def copy(self, source, destination):
        src, dst = self._existing(source), self.policy.resolve(destination)
        if dst.exists():
            raise FileExistsError("El destino ya existe.")
        if src.is_dir():
            if src in dst.parents:
                raise ValueError("No se puede copiar una carpeta dentro de sí misma.")
            shutil.copytree(src, dst)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        return self._relative(dst)

    def duplicate(self, source):
        src = self._existing(source)
        stem, suffix = (src.name, "") if src.is_dir() else (src.stem, src.suffix)
        index = 1
        while True:
            candidate = src.with_name(f"{stem} copia{'' if index == 1 else f' {index}'}{suffix}")
            if not candidate.exists():
                return self.copy(source, self._relative(candidate))
            index += 1

    def move_to_trash(self, source):
        src = self._existing(source)
        trash = self.policy.root / ".legna-trash"
        trash.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        destination = trash / f"{stamp}-{uuid4().hex[:8]}-{src.name}"
        shutil.move(str(src), str(destination))
        return {"trashed": self._relative(destination), "original": source}

    def _existing(self, relative_path):
        path = self.policy.resolve(relative_path)
        if path == self.policy.root:
            raise ValueError("La raíz del workspace no se puede modificar desde el Explorer.")
        if not path.exists():
            raise FileNotFoundError("El elemento ya no existe.")
        return path

    def _relative(self, path):
        return path.relative_to(self.policy.root).as_posix()
