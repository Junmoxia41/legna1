"""Application service that coordinates Legna chat without executing tools."""
from typing import Any, Dict, Optional

from ai.context_engine import ContextEngine
from brain.orchestrator import LegnaBrain
from ai.llm import LLMClient
from ai.personality_engine import PersonalityEngine
from memory.conversation_manager import ConversationManager
from memory.neural_memory import NeuralMemoryManager
from models.manager import ModelManager


class ChatService:
    """Persisted, context-aware chat service for the UI API."""

    def __init__(
        self,
        neural_memory: Optional[NeuralMemoryManager] = None,
        conversations: Optional[ConversationManager] = None,
        brain: Optional[LegnaBrain] = None,
        model_manager: Optional[ModelManager] = None,
    ) -> None:
        self.neural_memory = neural_memory or NeuralMemoryManager()
        self.conversations = conversations or ConversationManager()
        self.context_engine = ContextEngine(self.neural_memory)
        self.brain = brain or LegnaBrain()
        self.model_manager = model_manager or ModelManager()
        self.personality = PersonalityEngine()
        self.llm = LLMClient()

    def _build_prompt(self, message: str, conversation: Dict[str, Any], brain_instruction: str = "") -> str:
        context = self.context_engine.build_chat_context()
        history = conversation.get("messages", [])[-8:]
        history_text = "\n".join(
            f"{'Usuario' if item['role'] == 'user' else 'Legna'}: {item['content']}"
            for item in history
        )
        parts = [self.personality.get_personality_prompt(), brain_instruction]
        if context:
            parts.append(f"Contexto recordado (úsalo solo si es relevante): {context}")
        if history_text:
            parts.append(f"Conversación reciente:\n{history_text}")
        parts.append(f"Usuario: {message}\nLegna:")
        return "\n\n".join(parts)

    def process_message(self, message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        message = (message or "").strip()
        if not message:
            return {"ok": False, "error": "El mensaje no puede estar vacío."}
        if len(message) > 6000:
            return {"ok": False, "error": "El mensaje supera el límite de 6000 caracteres."}

        plan = self.brain.begin_task(message)
        conversation = self.conversations.get_conversation(conversation_id) if conversation_id else None
        if not conversation:
            conversation = self.conversations.create_conversation()
        conversation_id = conversation["id"]
        self.conversations.add_message(conversation_id, "user", message)
        conversation = self.conversations.get_conversation(conversation_id)

        selection = self.model_manager.select_for_task(plan["classification"]["primary"])
        try:
            execution = self.llm.preguntar_con_meta(
                self._build_prompt(message, conversation, self.brain.context_instruction(plan)),
                model=selection["model"],
            )
            answer = execution["response"]
            succeeded = execution["ok"]
        except Exception:
            execution = {"ok": False, "runtime": None, "model": selection["model"], "failures": []}
            answer = "Ha ocurrido un error al procesar la petición local."
            succeeded = False
        # Quality Agent: objective baseline. User feedback can later override it.
        automatic_score = 0.76 if succeeded and len(answer.strip()) >= 24 else (0.52 if succeeded else 0.05)
        rating = self.model_manager.record_outcome(execution.get("model"), plan["classification"]["primary"], automatic_score)
        self.brain.finish_task(plan["task"], succeeded)
        emotion = self.personality.detect_emotion(message)
        if not answer.startswith(("No puedo comunicarme", "Error:")):
            answer = self.personality.generate_emotional_response(answer, emotion)

        self.conversations.add_message(conversation_id, "legna", answer)
        return {
            "ok": True,
            "conversation_id": conversation_id,
            "response": answer,
            "context": self.context_engine.get_memory_summary(),
            "task": plan["task"],
            "execution": {"runtime": execution.get("runtime"), "model": execution.get("model"), "fallbacks": execution.get("failures", []), "rating": rating},
        }
