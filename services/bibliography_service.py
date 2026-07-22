"""Local biography/document import with transparent source annotations."""
import json
import re
from pathlib import Path


class BiographyService:
    FIELDS = ("nombre", "ubicacion", "idioma", "ocupacion", "habilidades", "intereses", "objetivos", "estilo_comunicacion", "bio")

    def __init__(self, neural_memory, chat_service):
        self.memory = neural_memory
        self.chat = chat_service

    def import_file(self, file_path):
        path = Path(file_path)
        if not path.is_file(): raise ValueError("El documento seleccionado no existe.")
        text = self._read(path)
        if not text.strip(): raise ValueError("No se pudo extraer texto útil del documento.")
        text = text[:45_000]
        prompt = (
            "Extrae únicamente datos biográficos explícitos del texto. No inventes datos. "
            "Devuelve JSON con las claves: nombre, ubicacion, idioma, ocupacion, habilidades, intereses, objetivos, estilo_comunicacion, bio. "
            "Usa cadena vacía cuando no exista evidencia. Texto:\n" + text
        )
        response = self.chat.llm.preguntar(prompt)
        fields = self._parse(response)
        source = f"Importado desde {path.name}"
        saved = []
        for key, value in fields.items():
            if value:
                self.memory.save_memory("perfil", key, value, confidence=0.6, notes=source)
                saved.append(key)
        # Always retain a short traceable summary, even if local model is unavailable.
        if not saved:
            self.memory.save_memory("perfil", "bio_importada", text[:2000], confidence=0.5, notes=source)
        return {"source": path.name, "saved": saved, "preview": fields, "text_length": len(text)}

    @staticmethod
    def _read(path):
        suffix = path.suffix.lower()
        if suffix in {".txt", ".md", ".rst"}: return path.read_text(encoding="utf-8", errors="replace")
        if suffix == ".pdf":
            from PyPDF2 import PdfReader
            return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
        if suffix == ".docx":
            from docx import Document
            return "\n".join(paragraph.text for paragraph in Document(str(path)).paragraphs)
        raise ValueError("Formato no soportado. Usa TXT, MD, PDF o DOCX.")

    def _parse(self, response):
        match = re.search(r"\{[\s\S]*\}", response)
        if not match: return {field: "" for field in self.FIELDS}
        try: raw = json.loads(match.group(0))
        except ValueError: return {field: "" for field in self.FIELDS}
        return {field: str(raw.get(field, "")).strip()[:4000] for field in self.FIELDS}
