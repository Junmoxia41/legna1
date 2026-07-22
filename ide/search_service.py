"""Bounded workspace search. It skips excluded directories and oversized files."""
import re
from pathlib import Path
from ide.policy import WorkspacePolicy


class SearchService:
    MAX_FILES = 8_000
    MAX_FILE_BYTES = 2 * 1024 * 1024
    MAX_RESULTS = 180

    def __init__(self, policy: WorkspacePolicy): self.policy = policy

    def files(self, query="", limit=80):
        query = (query or "").lower().strip()
        results = []
        for path in self._walk_files():
            relative = path.relative_to(self.policy.root).as_posix()
            if not query or query in relative.lower():
                results.append({"path": relative, "name": path.name})
                if len(results) >= min(limit, self.MAX_RESULTS): break
        return results

    def text(self, query, limit=100):
        query = (query or "").strip()
        if not query: return []
        needle = query.lower(); results = []
        for path in self._walk_files():
            if path.stat().st_size > self.MAX_FILE_BYTES: continue
            try: lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError: continue
            relative = path.relative_to(self.policy.root).as_posix()
            for line_no, line in enumerate(lines, 1):
                if needle in line.lower():
                    results.append({"path": relative, "line": line_no, "column": line.lower().find(needle)+1, "preview": line.strip()[:350]})
                    if len(results) >= min(limit, self.MAX_RESULTS): return results
        return results

    def symbols(self, relative_path):
        path = self.policy.resolve(relative_path)
        if path.stat().st_size > self.MAX_FILE_BYTES: return []
        text = path.read_text(encoding="utf-8", errors="replace")
        patterns = [
            ("class", re.compile(r"^\s*class\s+([A-Za-z_]\w*)", re.M)),
            ("function", re.compile(r"^\s*(?:async\s+)?def\s+([A-Za-z_]\w*)", re.M)),
            ("function", re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+([\w$]+)", re.M)),
            ("class", re.compile(r"^\s*(?:export\s+)?class\s+([\w$]+)", re.M)),
        ]
        symbols=[]
        for kind, pattern in patterns:
            for match in pattern.finditer(text):
                symbols.append({"name": match.group(1), "kind": kind, "line": text.count("\n", 0, match.start())+1, "column": match.start()-text.rfind("\n", 0, match.start())})
        return sorted(symbols, key=lambda entry: entry["line"])

    def _walk_files(self):
        count = 0
        for path in self.policy.root.rglob("*"):
            if count >= self.MAX_FILES: return
            if not path.is_file() or not self.policy.visible(path): continue
            count += 1
            yield path
