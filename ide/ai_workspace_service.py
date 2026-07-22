"""Contextual LEGNA Code proposals. Generated edits are never applied automatically."""
import difflib
import re
from datetime import datetime
from uuid import uuid4


class AIWorkspaceService:
    ACTIONS = {
        "explain": "Explica el código con precisión, incluyendo flujo, riesgos y sugerencias.",
        "document": "Propón una versión documentada. Devuelve exclusivamente el archivo completo entre ```.",
        "tests": "Propón pruebas útiles. Explica dónde crear el archivo y devuelve código entre ```.",
        "fix": "Corrige errores potenciales. Devuelve exclusivamente el archivo completo corregido entre ```.",
        "refactor": "Refactoriza conservando comportamiento. Devuelve exclusivamente el archivo completo entre ```.",
        "optimize": "Optimiza sin cambiar el comportamiento. Devuelve exclusivamente el archivo completo entre ```.",
    }

    def __init__(self, chat_service, document_service):
        self.chat_service = chat_service
        self.documents = document_service
        self.proposals = {}

    def propose(self, path, action, selection="", instruction=""):
        if action not in self.ACTIONS:
            raise ValueError("Acción de IA no soportada.")
        document = self.documents.read(path)
        source = selection.strip() or document["content"]
        if len(source) > 45_000:
            raise ValueError("La selección es demasiado grande para una propuesta segura.")
        plan = self.chat_service.brain.begin_task(f"Código: {action}. {instruction}")
        prompt = "\n\n".join([
            self.chat_service.personality.get_personality_prompt(),
            self.chat_service.brain.context_instruction(plan),
            "Actúas dentro de LEGNA IDE. No ejecutes comandos ni afirmes haber modificado archivos.",
            self.ACTIONS[action],
            f"Archivo: {path}",
            f"Instrucción adicional: {instruction or 'ninguna'}",
            "Código de contexto:\n```\n" + source + "\n```",
        ])
        selection_model = self.chat_service.model_manager.select_for_task("code")
        execution = self.chat_service.llm.preguntar_con_meta(prompt, model=selection_model["model"])
        success = execution["ok"]
        self.chat_service.brain.finish_task(plan["task"], success)
        rating = self.chat_service.model_manager.record_outcome(
            execution.get("model"), "code", 0.78 if success else 0.05, "ide_proposal"
        )
        response = execution["response"]
        proposed = self._extract_code(response) if action in {"document", "fix", "refactor", "optimize"} else None
        # Only full-file proposals are eligible to apply; selected snippets remain advisory.
        applicable = bool(proposed and not selection.strip())
        proposal_id = uuid4().hex
        proposal = {
            "id": proposal_id, "created_at": datetime.now().isoformat(), "path": path, "action": action,
            "response": response, "proposed_content": proposed, "applicable": applicable,
            "base_version": document["version"], "diff": self._diff(document["content"], proposed, path) if applicable else "",
            "execution": {"runtime": execution.get("runtime"), "model": execution.get("model"), "rating": rating},
        }
        self.proposals[proposal_id] = proposal
        return proposal

    def apply(self, proposal_id):
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError("Propuesta no encontrada o expirada.")
        if not proposal["applicable"]:
            raise ValueError("Esta propuesta no es un reemplazo completo aplicable.")
        saved = self.documents.save(proposal["path"], proposal["proposed_content"], proposal["base_version"])
        proposal["applied_at"] = datetime.now().isoformat()
        return saved

    @staticmethod
    def _extract_code(response):
        match = re.search(r"```(?:[\w+.-]+)?\s*\n([\s\S]*?)```", response)
        return match.group(1).strip("\n") if match else None

    @staticmethod
    def _diff(before, after, path):
        return "".join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                               fromfile=f"a/{path}", tofile=f"b/{path}"))
