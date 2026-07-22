"""Single facade exposed to the PyWebView IDE frontend."""
from pathlib import Path
from ide.ai_workspace_service import AIWorkspaceService
from ide.diagnostics_service import DiagnosticsService
from ide.document_service import DocumentService
from ide.filesystem_service import FilesystemService
from ide.git_service import GitService
from ide.plugin_service import PluginService
from ide.search_service import SearchService
from ide.session_service import SessionService
from ide.terminal_service import TerminalService
from ide.workspace_service import WorkspaceService


class IDEAPI:
    def __init__(self, project_manager, state_path, chat_service):
        self.workspaces = WorkspaceService(project_manager)
        self.sessions = SessionService(state_path)
        self.plugins = PluginService(Path(state_path).with_name("ide_plugins.json"))
        self.chat_service = chat_service
        self._services = {}

    def open_workspace(self, project_id):
        reference, policy = self.workspaces.open_project(project_id)
        if reference.id not in self._services:
            self._services[reference.id] = {
                "files": FilesystemService(policy), "documents": DocumentService(policy),
                "terminal": TerminalService(policy), "git": GitService(policy), "diagnostics": DiagnosticsService(policy),
                "ai": None, "search": SearchService(policy),
            }
            self._services[reference.id]["ai"] = AIWorkspaceService(self.chat_service, self._services[reference.id]["documents"])
        return reference.to_dict()

    def _get(self, workspace_id):
        if workspace_id not in self._services:
            self.open_workspace(workspace_id)
        return self._services[workspace_id]

    def list_directory(self, workspace_id, relative_path=""): return self._get(workspace_id)["files"].list_directory(relative_path)
    def create_file(self, workspace_id, relative_path, content=""):
        created = self._get(workspace_id)["files"].create_file(relative_path, content)
        self.plugins.observe_file(workspace_id, created)
        return created
    def create_directory(self, workspace_id, relative_path): return self._get(workspace_id)["files"].create_directory(relative_path)
    def rename_path(self, workspace_id, source, new_name): return self._get(workspace_id)["files"].rename(source, new_name)
    def copy_path(self, workspace_id, source, destination): return self._get(workspace_id)["files"].copy(source, destination)
    def move_path(self, workspace_id, source, destination): return self._get(workspace_id)["files"].move(source, destination)
    def duplicate_path(self, workspace_id, source): return self._get(workspace_id)["files"].duplicate(source)
    def trash_path(self, workspace_id, source): return self._get(workspace_id)["files"].move_to_trash(source)
    def read_document(self, workspace_id, relative_path): return self._get(workspace_id)["documents"].read(relative_path)
    def save_document(self, workspace_id, relative_path, content, expected_version=None): return self._get(workspace_id)["documents"].save(relative_path, content, expected_version)
    def create_terminal(self, workspace_id, label=None, relative_cwd=""): return self._get(workspace_id)["terminal"].create(label, relative_cwd)
    def list_terminals(self, workspace_id): return self._get(workspace_id)["terminal"].list()
    def run_terminal(self, workspace_id, session_id, command): return self._get(workspace_id)["terminal"].run(session_id, command)
    def close_terminal(self, workspace_id, session_id): return self._get(workspace_id)["terminal"].close(session_id)
    def git_status(self, workspace_id): return self._get(workspace_id)["git"].status()
    def git_diff(self, workspace_id, relative_path=None, staged=False): return self._get(workspace_id)["git"].diff(relative_path, staged)
    def git_stage(self, workspace_id, paths): return self._get(workspace_id)["git"].stage(paths)
    def git_unstage(self, workspace_id, paths): return self._get(workspace_id)["git"].unstage(paths)
    def git_commit(self, workspace_id, message): return self._get(workspace_id)["git"].commit(message)
    def git_branches(self, workspace_id): return self._get(workspace_id)["git"].branches()
    def diagnose_document(self, workspace_id, relative_path): return self._get(workspace_id)["diagnostics"].analyze(relative_path)
    def diagnose_workspace(self, workspace_id): return self._get(workspace_id)["diagnostics"].analyze_workspace()
    def ai_propose(self, workspace_id, path, action, selection="", instruction=""): return self._get(workspace_id)["ai"].propose(path, action, selection, instruction)
    def ai_apply_proposal(self, workspace_id, proposal_id): return self._get(workspace_id)["ai"].apply(proposal_id)
    def get_plugins(self, workspace_id): return self.plugins.get_plugins(workspace_id)
    def configure_language_plugin(self, workspace_id, group, enabled): return self.plugins.configure_group(workspace_id, group, enabled)
    def detect_language_plugin(self, workspace_id, filename): return self.plugins.observe_file(workspace_id, filename)
    def search_files(self, workspace_id, query=""): return self._get(workspace_id)["search"].files(query)
    def search_text(self, workspace_id, query): return self._get(workspace_id)["search"].text(query)
    def search_symbols(self, workspace_id, relative_path): return self._get(workspace_id)["search"].symbols(relative_path)
    def get_session(self): return self.sessions.load()
    def save_session(self, state): return self.sessions.save(state)
