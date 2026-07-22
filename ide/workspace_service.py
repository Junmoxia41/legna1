"""Adapter over the existing ProjectManager; preserves registered projects."""
from ide.models import WorkspaceRef
from ide.policy import WorkspacePolicy

class WorkspaceService:
    def __init__(self, project_manager): self.project_manager = project_manager
    def open_project(self, project_id):
        project = self.project_manager.get_project(project_id)
        if not project: raise ValueError('Proyecto no encontrado.')
        ref = WorkspaceRef(project['id'], project['name'], project['path'])
        return ref, WorkspacePolicy(ref.root)
