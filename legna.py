"""
LEGNA v3.0 - Neural Companion
Único archivo de ejecución (PyWebView)
Integra: Workspace, Chat, Memoria Neuronal, Monaco Editor, Terminal Real
"""

import webview
import os
from pathlib import Path
from workspace.project_manager import ProjectManager
from memory.neural_memory import NeuralMemoryManager
from memory.conversation_manager import ConversationManager

BASE_DIR = Path(__file__).parent.resolve()
os.chdir(BASE_DIR)

# Instancias globales
project_manager = ProjectManager()
neural_memory = NeuralMemoryManager()
conversation_manager = ConversationManager()


class LegnaAPI:
    """API expuesta a JavaScript"""

    # === PROYECTOS ===
    def get_projects(self):
        return project_manager.get_all_projects()

    def create_project(self, name):
        return project_manager.create_new_project(name)

    def import_project(self, path, move=True):
        return project_manager.import_project(path, move=move)

    # === MEMORIA NEURONAL ===
    def get_neural_memories(self):
        return neural_memory.get_all_memories()

    def save_neural_memory(self, category, key, value):
        return neural_memory.save_memory(category, key, value)

    # === CONVERSACIONES ===
    def get_conversations(self):
        return conversation_manager.get_all_conversations()

    def create_conversation(self):
        return conversation_manager.create_conversation()

    # === CHAT ===
    def process_chat(self, message):
        # Respuesta simple por ahora (puedes conectar con LLM real)
        return f"Entendido. He procesado tu mensaje: {message}"

    # === HERRAMIENTAS ===
    def open_monaco(self, file_path=None):
        """Abre Monaco Editor en una nueva ventana"""
        from ui.monaco_webview import create_monaco_window
        create_monaco_window(file_path)
        return "Monaco Editor abierto"

    def open_terminal(self):
        """Abre Terminal Real"""
        from ui.real_terminal_window import create_terminal_window
        create_terminal_window()
        return "Terminal Real abierta"


def run():
    print("🧠 LEGNA v3.0 iniciando con PyWebView...")

    html_path = BASE_DIR / "ui" / "index.html"
    if not html_path.exists():
        print("Error: index.html no encontrado")
        return

    window = webview.create_window(
        "LEGNA v3.0 | Neural Interface",
        url=str(html_path),
        width=1400,
        height=900,
        resizable=True,
        background_color='#010206'
    )

    api = LegnaAPI()
    window.expose(
        api.get_projects,
        api.create_project,
        api.import_project,
        api.get_neural_memories,
        api.save_neural_memory,
        api.get_conversations,
        api.create_conversation,
        api.process_chat,
        api.open_monaco,
        api.open_terminal
    )

    webview.start(debug=False)


if __name__ == "__main__":
    run()