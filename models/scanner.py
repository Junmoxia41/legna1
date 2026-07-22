"""Safe local GGUF catalog scanner; it never loads a model into memory."""
from pathlib import Path
from typing import Dict, List


class ModelScanner:
    def __init__(self, models_dir):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def scan(self) -> List[Dict]:
        models = []
        for path in sorted(self.models_dir.rglob("*")):
            if not path.is_file() or path.suffix.lower() != ".gguf":
                continue
            stat = path.stat()
            # GGUF starts with this magic when it is a valid uncompressed file.
            try:
                with path.open("rb") as handle:
                    valid_magic = handle.read(4) == b"GGUF"
            except OSError:
                valid_magic = False
            models.append({
                "id": str(path.relative_to(self.models_dir)).replace("\\", "/"),
                "name": path.stem,
                "path": str(path),
                "size_bytes": stat.st_size,
                "size_gb": round(stat.st_size / 1024 ** 3, 2),
                "format": "GGUF",
                "valid": valid_magic,
                "type": self._infer_type(path.stem),
            })
        return models

    @staticmethod
    def _infer_type(name: str) -> str:
        lowered = name.lower()
        if any(key in lowered for key in ("coder", "code", "deepseek")):
            return "code"
        if any(key in lowered for key in ("vision", "llava", "vl")):
            return "vision"
        return "general"
