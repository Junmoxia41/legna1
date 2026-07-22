"""LEGNA v3.0 - PyWebView desktop interface."""
import os
import platform
import subprocess
import sys
import ctypes
from pathlib import Path
from typing import Optional

import psutil
import webview

from agents.registry import AgentRegistry
from ide.api import IDEAPI
from ide.policy import WorkspacePolicy
from ide.terminal_service import TerminalService
from brain.orchestrator import LegnaBrain
from models.manager import ModelManager
from memory.conversation_manager import ConversationManager
from memory.neural_memory import NeuralMemoryManager
from services.chat_service import ChatService
from services.bibliography_service import BiographyService
from workspace.project_manager import ProjectManager

def is_process_elevated():
    if os.name != "nt":
        return False
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


BASE_DIR = Path(__file__).parent.resolve()
os.chdir(BASE_DIR)

project_manager = ProjectManager(workspace_root=BASE_DIR / "workspace")
neural_memory = NeuralMemoryManager(db_path=BASE_DIR / "database" / "neural_memory.json")
conversation_manager = ConversationManager(storage_path=BASE_DIR / "database" / "conversations.json")
agent_registry = AgentRegistry()
legna_brain = LegnaBrain(agent_registry)
# One shared ModelManager serves both the chat router and the Agent OS dashboard.
model_manager = ModelManager(models_dir=BASE_DIR / "data" / "models")
chat_service = ChatService(neural_memory, conversation_manager, legna_brain, model_manager)
biography_service = BiographyService(neural_memory, chat_service)
ide_api = IDEAPI(project_manager, BASE_DIR / "database" / "ide_session.json", chat_service)


class LegnaAPI:
    """Small, validated API exposed to the local PyWebView interface."""

    def __init__(self) -> None:
        # Prime psutil so the following non-blocking sample is meaningful.
        psutil.cpu_percent(interval=None)

    def get_system_stats(self):
        memory = psutil.virtual_memory()
        return {
            # A short sampling interval produces a real value on Windows; the
            # non-blocking first sample can otherwise remain at 0.0.
            "cpu_percent": round(psutil.cpu_percent(interval=0.2), 1),
            "ram_percent": round(memory.percent, 1),
            "ram_used_gb": round(memory.used / (1024 ** 3), 1),
            "ram_total_gb": round(memory.total / (1024 ** 3), 1),
            "host": platform.node() or "Equipo local",
            "platform": f"{platform.system()} {platform.release()}",
            "status": "ACTIVE",
        }

    # Agent OS / local model catalog
    def get_agents_dashboard(self):
        models = model_manager.dashboard()
        brain = legna_brain.dashboard()
        for agent in brain["agents"]:
            agent["assigned_model"] = models["assignments"].get(agent["id"], "auto")
        return {**brain, "models": models}

    def rescan_models(self):
        return model_manager.dashboard()

    # IDE process is selected before it starts; the child IDE never asks twice.
    def open_ide(self, project_id, mode="standard"):
        if not project_manager.get_project(project_id):
            raise ValueError("Proyecto no encontrado.")
        args = [str(BASE_DIR / "legna.py"), "--ide", str(project_id)]
        if mode == "admin":
            if os.name != "nt":
                raise RuntimeError("El modo administrador solo está disponible en Windows.")
            quoted_args = " ".join(f'"{arg}"' for arg in args)
            subprocess.Popen(["powershell", "-NoProfile", "-Command", f"Start-Process -FilePath '{sys.executable}' -ArgumentList '{quoted_args}' -Verb RunAs"])
            return {"ok": True, "message": "Windows solicitará confirmación de administrador."}
        subprocess.Popen([sys.executable, *args], cwd=BASE_DIR)
        return {"ok": True, "message": "LEGNA IDE se abrió en modo estándar."}

    def select_model_file(self):
        if not hasattr(self, "window"):
            raise RuntimeError("El selector de modelos no está disponible.")
        result = self.window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=("Modelos GGUF (*.gguf)",))
        return result[0] if result else None

    def import_model(self, file_path):
        return model_manager.import_gguf(file_path)

    def assign_agent_model(self, agent_id, model_id):
        return model_manager.assign_agent(agent_id, model_id)

    def select_project_directory(self):
        if not hasattr(self, "window"):
            raise RuntimeError("El selector de carpetas no está disponible.")
        result = self.window.create_file_dialog(webview.FOLDER_DIALOG)
        return result[0] if result else None

    def ide_get_execution_mode(self):
        return {"mode": "admin" if is_process_elevated() else "standard", "elevated": is_process_elevated()}

    def ide_request_admin_mode(self, project_id):
        if os.name != "nt":
            raise RuntimeError("La elevación de Windows solo está disponible en Windows.")
        if not project_manager.get_project(project_id):
            raise ValueError("Proyecto no encontrado.")
        if is_process_elevated():
            return {"started": False, "message": "Esta instancia ya se ejecuta como administrador."}
        args = f'"{BASE_DIR / "legna.py"}" --ide "{project_id}" --elevated'
        subprocess.Popen(["powershell", "-NoProfile", "-Command", f"Start-Process -FilePath '{sys.executable}' -ArgumentList '{args}' -Verb RunAs"])
        return {"started": True, "message": "Windows solicitará confirmación de administrador."}

    # IDE workspace API. The frontend never accesses files directly.
    def ide_open_workspace(self, project_id): return ide_api.open_workspace(project_id)
    def ide_list_directory(self, workspace_id, relative_path=""): return ide_api.list_directory(workspace_id, relative_path)
    def ide_create_file(self, workspace_id, relative_path, content=""): return ide_api.create_file(workspace_id, relative_path, content)
    def ide_create_directory(self, workspace_id, relative_path): return ide_api.create_directory(workspace_id, relative_path)
    def ide_rename_path(self, workspace_id, source, new_name): return ide_api.rename_path(workspace_id, source, new_name)
    def ide_copy_path(self, workspace_id, source, destination): return ide_api.copy_path(workspace_id, source, destination)
    def ide_move_path(self, workspace_id, source, destination): return ide_api.move_path(workspace_id, source, destination)
    def ide_duplicate_path(self, workspace_id, source): return ide_api.duplicate_path(workspace_id, source)
    def ide_trash_path(self, workspace_id, source): return ide_api.trash_path(workspace_id, source)
    def ide_create_terminal(self, workspace_id, label=None, relative_cwd=""): return ide_api.create_terminal(workspace_id, label, relative_cwd)
    def ide_list_terminals(self, workspace_id): return ide_api.list_terminals(workspace_id)
    def ide_run_terminal(self, workspace_id, session_id, command): return ide_api.run_terminal(workspace_id, session_id, command)
    def ide_close_terminal(self, workspace_id, session_id): return ide_api.close_terminal(workspace_id, session_id)
    def ide_git_status(self, workspace_id): return ide_api.git_status(workspace_id)
    def ide_git_diff(self, workspace_id, relative_path=None, staged=False): return ide_api.git_diff(workspace_id, relative_path, staged)
    def ide_git_stage(self, workspace_id, paths): return ide_api.git_stage(workspace_id, paths)
    def ide_git_unstage(self, workspace_id, paths): return ide_api.git_unstage(workspace_id, paths)
    def ide_git_commit(self, workspace_id, message): return ide_api.git_commit(workspace_id, message)
    def ide_git_branches(self, workspace_id): return ide_api.git_branches(workspace_id)
    def ide_diagnose_document(self, workspace_id, relative_path): return ide_api.diagnose_document(workspace_id, relative_path)
    def ide_diagnose_workspace(self, workspace_id): return ide_api.diagnose_workspace(workspace_id)
    def ide_ai_propose(self, workspace_id, path, action, selection="", instruction=""): return ide_api.ai_propose(workspace_id, path, action, selection, instruction)
    def ide_ai_apply_proposal(self, workspace_id, proposal_id): return ide_api.ai_apply_proposal(workspace_id, proposal_id)
    def ide_get_plugins(self, workspace_id): return ide_api.get_plugins(workspace_id)
    def ide_configure_language_plugin(self, workspace_id, group, enabled): return ide_api.configure_language_plugin(workspace_id, group, enabled)
    def ide_detect_language_plugin(self, workspace_id, filename): return ide_api.detect_language_plugin(workspace_id, filename)
    def ide_search_files(self, workspace_id, query=""): return ide_api.search_files(workspace_id, query)
    def ide_search_text(self, workspace_id, query): return ide_api.search_text(workspace_id, query)
    def ide_search_symbols(self, workspace_id, relative_path): return ide_api.search_symbols(workspace_id, relative_path)
    def ide_read_document(self, workspace_id, relative_path): return ide_api.read_document(workspace_id, relative_path)
    def ide_save_document(self, workspace_id, relative_path, content, expected_version=None): return ide_api.save_document(workspace_id, relative_path, content, expected_version)
    def ide_get_session(self): return ide_api.get_session()
    def ide_save_session(self, state): return ide_api.save_session(state)

    # Projects
    def get_projects(self):
        return project_manager.get_all_projects()

    def create_project(self, name):
        name = (name or "").strip()
        if not name:
            raise ValueError("El nombre del proyecto es obligatorio.")
        return project_manager.create_new_project(name)

    def import_project(self, path, move=True):
        return project_manager.import_project(path, move=bool(move))

    # Neural memory and profile
    def get_neural_memories(self):
        return neural_memory.get_all_memories()

    def save_neural_memory(self, category, key, value):
        return neural_memory.save_memory(category, key, value)

    def get_profile(self):
        fields = ("nombre", "segundo_nombre", "edad", "ubicacion", "pronombres", "idioma", "zona_horaria", "ocupacion", "habilidades", "intereses", "objetivos", "estilo_comunicacion", "accesibilidad", "preferencias", "bio")
        values = {m["key"]: m["value"] for m in neural_memory.get_memories_by_category("perfil")}
        identity = neural_memory.get_identity()
        profile = {field: values.get(field, "") for field in fields}
        profile["nombre"] = identity.get("nombre") if identity.get("nombre") != "Airien" else profile["nombre"]
        profile["segundo_nombre"] = identity.get("segundo_nombre") or profile["segundo_nombre"]
        profile["edad"] = identity.get("edad") or profile["edad"]
        return profile

    def save_profile(self, profile):
        if not isinstance(profile, dict):
            raise ValueError("El perfil debe ser un objeto.")
        fields = ("nombre", "segundo_nombre", "edad", "ubicacion", "pronombres", "idioma", "zona_horaria", "ocupacion", "habilidades", "intereses", "objetivos", "estilo_comunicacion", "accesibilidad", "preferencias", "bio")
        saved = {}
        for field in fields:
            value = str(profile.get(field, "")).strip()
            if value:
                category = "nombre" if field in ("nombre", "segundo_nombre") else ("edad" if field == "edad" else "perfil")
                saved[field] = neural_memory.save_memory(category, field, value, notes="Perfil proporcionado por el usuario")
        return {"ok": True, "profile": self.get_profile(), "saved": list(saved)}

    def select_biography_file(self):
        if not hasattr(self, "window"):
            raise RuntimeError("El selector de archivos no está disponible.")
        result = self.window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=("Documentos (*.txt;*.md;*.pdf;*.docx)",))
        return result[0] if result else None

    def import_biography(self, file_path):
        return biography_service.import_file(file_path)

    # Conversations and chat
    def get_conversations(self):
        return conversation_manager.get_all_conversations()

    def get_conversation(self, conversation_id):
        return conversation_manager.get_conversation(conversation_id)

    def create_conversation(self):
        return conversation_manager.create_conversation()

    def process_chat(self, message, conversation_id: Optional[str] = None):
        # Tools are deliberately not enabled from free-form chat.
        return chat_service.process_message(message, conversation_id)

    # Compatibility actions retained for existing dashboard buttons.
    def open_monaco(self, file_path=None):
        return "El editor Monaco está integrado en LEGNA IDE. Abre un proyecto desde Workspace."

    def open_terminal(self, mode="standard"):
        args = [str(BASE_DIR / "legna.py"), "--terminal"]
        if mode == "admin":
            if os.name != "nt": raise RuntimeError("El modo administrador solo está disponible en Windows.")
            quoted_args = " ".join(f'"{arg}"' for arg in args)
            subprocess.Popen(["powershell", "-NoProfile", "-Command", f"Start-Process -FilePath '{sys.executable}' -ArgumentList '{quoted_args}' -Verb RunAs"])
            return {"ok": True, "message": "Windows solicitará confirmación de administrador."}
        subprocess.Popen([sys.executable, *args], cwd=BASE_DIR)
        return {"ok": True, "message": "Terminal abierta en modo estándar."}


def run():
    html_path = BASE_DIR / "ui" / "index.html"
    if not html_path.exists():
        raise FileNotFoundError("ui/index.html no encontrado")
    window = webview.create_window(
        "LEGNA v3.0 | Neural Interface", url=str(html_path), width=1400,
        height=900, resizable=True, background_color="#010206",
    )
    api = LegnaAPI()
    api.window = window
    for method in (
        api.get_system_stats, api.get_agents_dashboard, api.rescan_models, api.open_ide, api.select_model_file, api.import_model, api.assign_agent_model, api.select_project_directory,
        api.ide_open_workspace, api.ide_list_directory, api.ide_create_file, api.ide_create_directory,
        api.ide_rename_path, api.ide_copy_path, api.ide_move_path, api.ide_duplicate_path, api.ide_trash_path,
        api.ide_create_terminal, api.ide_list_terminals, api.ide_run_terminal, api.ide_close_terminal,
        api.ide_git_status, api.ide_git_diff, api.ide_git_stage, api.ide_git_unstage, api.ide_git_commit, api.ide_git_branches,
        api.ide_diagnose_document, api.ide_diagnose_workspace, api.ide_ai_propose, api.ide_ai_apply_proposal,
        api.ide_get_plugins, api.ide_configure_language_plugin, api.ide_detect_language_plugin,
        api.ide_search_files, api.ide_search_text, api.ide_search_symbols, api.ide_read_document, api.ide_save_document, api.ide_get_session, api.ide_save_session, api.get_projects, api.create_project, api.import_project,
        api.get_neural_memories, api.save_neural_memory, api.get_profile, api.save_profile, api.select_biography_file, api.import_biography,
        api.get_conversations, api.get_conversation, api.create_conversation, api.process_chat,
        api.open_monaco, api.open_terminal,
    ):
        window.expose(method)
    webview.start(debug=False)


class TerminalWindowAPI:
    def __init__(self):
        self.terminal = TerminalService(WorkspacePolicy(BASE_DIR))
        self.session = self.terminal.create("Terminal LEGNA")

    def terminal_info(self):
        return {"mode": "admin" if is_process_elevated() else "standard", "cwd": self.session["cwd"]}

    def terminal_run(self, command):
        return self.terminal.run(self.session["id"], command)


def run_terminal_window():
    html_path = BASE_DIR / "ui" / "terminal" / "index.html"
    window = webview.create_window("LEGNA Terminal", url=str(html_path), width=1000, height=650, resizable=True, background_color="#020409")
    api = TerminalWindowAPI()
    window.expose(api.terminal_info, api.terminal_run)
    webview.start(debug=False)


class IDEWindowAPI(LegnaAPI):
    """Dedicated API for a child IDE process; avoids query parameters on file URLs."""
    def __init__(self, project_id):
        super().__init__()
        self.project_id = project_id

    def ide_get_launch_project(self):
        return self.project_id


def run_ide_window(project_id):
    html_path = BASE_DIR / "ui" / "ide" / "index.html"
    if not html_path.exists():
        raise FileNotFoundError(f"IDE no encontrado: {html_path}")
    # Pass a plain local path. Windows WebView can reject file:// URLs with a query string.
    window = webview.create_window("LEGNA IDE | Neural Workspace", url=str(html_path), width=1500, height=960, resizable=True, background_color="#020409")
    api = IDEWindowAPI(project_id)
    for method in (
        api.ide_get_launch_project, api.ide_open_workspace, api.ide_list_directory, api.ide_create_file, api.ide_create_directory,
        api.ide_rename_path, api.ide_copy_path, api.ide_move_path, api.ide_duplicate_path, api.ide_trash_path,
        api.ide_create_terminal, api.ide_list_terminals, api.ide_run_terminal, api.ide_close_terminal,
        api.ide_git_status, api.ide_git_diff, api.ide_git_stage, api.ide_git_unstage, api.ide_git_commit, api.ide_git_branches,
        api.ide_diagnose_document, api.ide_diagnose_workspace, api.ide_ai_propose, api.ide_ai_apply_proposal,
        api.ide_get_plugins, api.ide_configure_language_plugin, api.ide_detect_language_plugin,
        api.ide_search_files, api.ide_search_text, api.ide_search_symbols, api.ide_read_document, api.ide_save_document,
        api.ide_get_session, api.ide_save_session,
    ): window.expose(method)
    webview.start(debug=False)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--terminal":
        run_terminal_window()
    elif len(sys.argv) >= 3 and sys.argv[1] == "--ide":
        run_ide_window(sys.argv[2])
    else:
        run()
