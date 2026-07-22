"""
Chat Screen - Legna v2.0
Full chat experience with:
- Dynamic right panel (Conversations)
- Human greetings using GreetingEngine
- Integration with neural memory
"""

import flet as ft
from ui.conversation_panel import ConversationPanel
from ai.greeting_engine import GreetingEngine
from memory.neural_memory import NeuralMemoryManager
from ai.project_analyzer import ProjectAnalyzer
from ai.context_engine import ContextEngine
from memory.conversation_manager import ConversationManager
from ai.deep_project_analyzer import DeepProjectAnalyzer
from ai.model_router import ModelRouter
from ai.personality_engine import PersonalityEngine
from ui.code_editor import LegnaCodeEditor


class ChatScreen:
    def __init__(self, page: ft.Page, assistant=None):
        self.page = page
        self.assistant = assistant
        
        # Neural Memory + Greeting Engine + Project Analyzer + Context + Conversations
        self.neural_memory = NeuralMemoryManager()
        self.greeting_engine = GreetingEngine(neural_memory=self.neural_memory)
        self.project_analyzer = ProjectAnalyzer()
        self.deep_analyzer = DeepProjectAnalyzer()
        self.context_engine = ContextEngine(self.neural_memory)
        self.conversation_manager = ConversationManager()
        
        # Multi-model + Personality
        self.model_router = ModelRouter()
        self.personality = PersonalityEngine()
        
        # Current active conversation
        self.current_conversation = None
        
        self.chat_messages = ft.ListView(expand=True, spacing=12, padding=20, auto_scroll=True)
        self.input_field = ft.TextField(
            hint_text="Escribe tu mensaje a Legna...",
            border=ft.InputBorder.NONE,
            expand=True,
            on_submit=self._send_message,
            text_style=ft.TextStyle(size=14)
        )

        # Right panel - Conversations
        self.right_panel = ConversationPanel(
            page=page,
            on_new_chat=self._start_new_conversation,
            on_open_chat=self._open_saved_conversation
        )

    def build(self):
        # Initial greeting (human and contextual)
        self._add_initial_greeting()

        # Chat input bar
        input_bar = ft.Container(
            padding=20,
            bgcolor="#05060A",
            border=ft.Border(top=ft.BorderSide(1, "#1F2633")),
            content=ft.Row([
                self.input_field,
                ft.IconButton(
                    icon=ft.Icons.SEND,
                    icon_color="#00D9FF",
                    on_click=self._send_message
                )
            ], spacing=8)
        )

        # Main chat area
        chat_area = ft.Column([
            self.chat_messages,
            input_bar
        ], expand=True)

        # Full layout with dynamic right panel
        return ft.Row([
            chat_area,
            self.right_panel.build()
        ], expand=True, spacing=0)

    def _add_initial_greeting(self):
        greeting = self.greeting_engine.get_greeting()
        
        # Create new persisted conversation
        self.current_conversation = self.conversation_manager.create_conversation()
        
        self.chat_messages.controls.append(
            ft.Container(
                content=ft.Text(greeting, size=14, color="#00D9FF"),
                bgcolor="#0A0B10",
                padding=16,
                border_radius=16,
                border=ft.Border(left=ft.BorderSide(3, "#00D9FF"))
            )
        )
        self.page.update()

    def _send_message(self, e=None):
        text = self.input_field.value.strip()
        if not text:
            return

        # Save user message to current conversation
        if self.current_conversation:
            self.conversation_manager.add_message(self.current_conversation["id"], "user", text)

        # User message
        self.chat_messages.controls.append(
            ft.Container(
                content=ft.Text(text, size=14, color="white"),
                bgcolor="#1A1C25",
                padding=14,
                border_radius=16,
                alignment=ft.alignment.center_right
            )
        )
        self.input_field.value = ""
        self.page.update()

        # Simulate Legna response + save it
        self._simulate_legna_response(text)

    def _simulate_legna_response(self, user_text: str):
        """Smart response using Model Router + Personality + Deep Analysis"""
        lower_text = user_text.lower()
        response = ""

        # Detect emotion first
        emotion = self.personality.detect_emotion(user_text)
        self.personality.set_mood(emotion)

        # === PROJECT ANALYSIS DETECTION ===
        project_intent = self.project_analyzer.detect_project_intent(user_text)
        if project_intent["action"] == "open_project":
            proj = project_intent["project"]
            response = project_intent["message"]
            
            self.chat_messages.controls.append(
                ft.Container(
                    content=ft.Text(response, size=14, color="#00D9FF"),
                    bgcolor="#0A0B10",
                    padding=16,
                    border_radius=16,
                    border=ft.Border(left=ft.BorderSide(3, "#00D9FF"))
                )
            )
            self.page.update()
            
            self._open_editor_from_chat(proj)
            return

        # === DEEP PROJECT ANALYSIS (uses powerful model) ===
        if any(word in lower_text for word in ["analiza", "analizar", "estructura", "dependencias", "proyecto"]):
            model_info = self.model_router.get_model_info("deep_analysis")
            
            if "legna" in lower_text or "legna1" in lower_text:
                for p in self.deep_analyzer.pm.get_all_projects():
                    if "legna" in p["name"].lower():
                        summary = self.deep_analyzer.get_analysis_summary(p["id"])
                        response = f"{model_info}\n\n**Análisis profundo:**\n\n{summary}"
                        break
                else:
                    response = "No encontré el proyecto 'legna1'. ¿Quieres que analice otro?"
            else:
                response = f"{model_info}\n\nDime qué proyecto quieres que analice en profundidad."

            # Apply personality
            response = self.personality.generate_emotional_response(response, emotion)
            
            self.chat_messages.controls.append(
                ft.Container(
                    content=ft.Text(response, size=14, color="#00D9FF"),
                    bgcolor="#0A0B10",
                    padding=16,
                    border_radius=16,
                    border=ft.Border(left=ft.BorderSide(3, "#00D9FF"))
                )
            )
            self.page.update()
            return

        # === NORMAL SMART RESPONSE ===
        # Choose model based on task
        model = self.model_router.get_model_for_task("chat")
        
        # Build rich context
        context = self.context_engine.build_chat_context()
        
        if "me llamo" in lower_text or "mi nombre es" in lower_text:
            parts = user_text.split()
            if len(parts) >= 3:
                nombre = parts[-1].capitalize()
                self.neural_memory.save_memory("nombre", "nombre", nombre, 0.95)
                response = f"¡Perfecto! Ahora sé que te llamas {nombre}. ¿Tienes segundo nombre?"
        
        elif "segundo nombre" in lower_text:
            words = user_text.split()
            if len(words) >= 2:
                segundo = words[-1].capitalize()
                self.neural_memory.save_memory("nombre", "segundo_nombre", segundo, 0.9)
                response = f"¡Entendido! Tu segundo nombre es {segundo}."
        
        elif "tengo" in lower_text and "años" in lower_text:
            import re
            match = re.search(r'(\d+)', user_text)
            if match:
                edad = match.group(1)
                self.neural_memory.save_memory("edad", "edad", edad, 0.9)
                response = f"¡Genial! Ahora sé que tienes {edad} años."
        
        elif "comando" in lower_text:
            cmd = user_text.strip().split()[0]
            self.neural_memory.save_memory("comando", cmd, "Comando aprendido", 0.85)
            response = f"¡Perfecto! Voy a recordar el comando `{cmd}`."
        
        else:
            if context:
                response = f"{context} ¿En qué más puedo ayudarte?"
            else:
                response = "Entendido. Voy guardando todo en mi cerebro neuronal."

        # Apply personality and emotion
        response = self.personality.generate_emotional_response(response, emotion)

        # Show response with model info (optional)
        final_response = f"{response}"

        self.chat_messages.controls.append(
            ft.Container(
                content=ft.Text(final_response, size=14, color="#00D9FF"),
                bgcolor="#0A0B10",
                padding=16,
                border_radius=16,
                border=ft.Border(left=ft.BorderSide(3, "#00D9FF"))
            )
        )
        self.page.update()

        # === AUTO LEARNING ===
        if "me llamo" in lower_text or "mi nombre es" in lower_text:
            parts = user_text.split()
            if len(parts) >= 3:
                nombre = parts[-1].capitalize()
                self.neural_memory.save_memory("nombre", "nombre", nombre, 0.95)
                response = f"¡Perfecto! Ahora sé que te llamas {nombre}. ¿Tienes segundo nombre?"
        
        elif "segundo nombre" in lower_text:
            words = user_text.split()
            if len(words) >= 2:
                segundo = words[-1].capitalize()
                self.neural_memory.save_memory("nombre", "segundo_nombre", segundo, 0.9)
                response = f"¡Entendido! Tu segundo nombre es {segundo}. ¿Qué edad tienes?"
        
        elif "tengo" in lower_text and "años" in lower_text:
            import re
            match = re.search(r'(\d+)', user_text)
            if match:
                edad = match.group(1)
                self.neural_memory.save_memory("edad", "edad", edad, 0.9)
                response = f"¡Genial! Ahora sé que tienes {edad} años."
        
        elif "comando" in lower_text or user_text.strip().startswith("ipconfig"):
            cmd = user_text.strip().split()[0]
            self.neural_memory.save_memory("comando", cmd, "Comando aprendido", 0.85)
            response = f"¡Perfecto! Voy a recordar el comando `{cmd}`."

        # === CONTEXT-AWARE RESPONSE ===
        else:
            context = self.context_engine.build_chat_context()
            
            if context:
                response = f"{context} ¿En qué más puedo ayudarte hoy?"
            else:
                response = "Entendido. Voy guardando todo en mi cerebro neuronal."

        # Show response
        self.chat_messages.controls.append(
            ft.Container(
                content=ft.Text(response, size=14, color="#00D9FF"),
                bgcolor="#0A0B10",
                padding=16,
                border_radius=16,
                border=ft.Border(left=ft.BorderSide(3, "#00D9FF"))
            )
        )
        self.page.update()

    def _start_new_conversation(self):
        """Start fresh conversation with new greeting"""
        self.chat_messages.controls.clear()
        self._add_initial_greeting()
        self.page.snack_bar = ft.SnackBar(ft.Text("Nueva conversación iniciada"))
        self.page.snack_bar.open = True
        self.page.update()

    def _open_saved_conversation(self, conv: dict):
        """Load a previous conversation"""
        self.chat_messages.controls.clear()
        
        # Add header
        self.chat_messages.controls.append(
            ft.Text(f"📁 {conv['title']}", size=12, color="#667788", weight="bold")
        )
        
        # Add a sample message from that conversation
        self.chat_messages.controls.append(
            ft.Container(
                content=ft.Text(conv["last_message"], size=14, color="#00D9FF"),
                bgcolor="#0A0B10",
                padding=16,
                border_radius=16,
                border=ft.Border(left=ft.BorderSide(3, "#00D9FF"))
            )
        )
        self.page.update()

    def _open_editor_from_chat(self, project: dict):
        """Opens the code editor from chat context"""
        from ui.code_editor import LegnaCodeEditor
        
        editor = LegnaCodeEditor(self.page, project)
        editor_screen = editor.build()
        
        self.page.controls.clear()
        self.page.add(editor_screen)
        self.page.update()