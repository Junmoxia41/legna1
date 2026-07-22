"""
Workspace View - Legna v2.0
Big hero card + Project import + Project list
Uses custom SVG icons (no emojis)
"""

import flet as ft
from ui.svg import *  # Custom SVGs
from workspace.project_manager import ProjectManager
import os


class WorkspaceScreen:
    def __init__(self, page: ft.Page, assistant=None):
        self.page = page
        self.assistant = assistant
        self.pm = ProjectManager()
        self.projects_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=12)

    def build(self):
        # === HERO CARD: Crear Nuevo Proyecto ===
        hero_card = ft.Container(
            width=480,
            height=220,
            bgcolor="#0A0B10",
            border=ft.Border(
                ft.BorderSide(2, "#00D9FF"),
                ft.BorderSide(2, "#00D9FF"),
                ft.BorderSide(2, "#00D9FF"),
                ft.BorderSide(2, "#00D9FF")
            ),
            border_radius=24,
            padding=30,
            content=ft.Column([
                ft.Row([
                    ft.Image(src="/home/user/legna1/ui/svg/folder_plus.svg", width=72, height=72),
                    ft.Container(width=20),
                    ft.Column([
                        ft.Text("Crear Nuevo Proyecto", size=26, weight="bold", color="#00D9FF"),
                        ft.Text("Inicia un nuevo entorno de trabajo\ncon estructura profesional.", 
                                size=14, color="#8899AA", max_lines=2)
                    ], spacing=6)
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                
                ft.Container(height=25),
                
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("CREAR PROYECTO", size=15, weight="bold", color="white"),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    style=ft.ButtonStyle(
                        bgcolor="#00D9FF",
                        color="white",
                        padding=ft.padding.symmetric(horizontal=50, vertical=14),
                        shape=ft.RoundedRectangleBorder(radius=14)
                    ),
                    on_click=self._create_new_project
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        # === IMPORT BUTTON ===
        import_btn = ft.ElevatedButton(
            content=ft.Row([
                ft.Image(src="/home/user/legna1/ui/svg/import.svg", width=28, height=28),
                ft.Container(width=12),
                ft.Text("IMPORTAR PROYECTO", size=15, weight="bold")
            ], alignment=ft.MainAxisAlignment.CENTER),
            style=ft.ButtonStyle(
                bgcolor="#1A1C25",
                color="#00D9FF",
                padding=ft.padding.symmetric(horizontal=32, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=14),
                side=ft.BorderSide(1.5, "#00D9FF")
            ),
            on_click=self._import_project_dialog
        )

        # === PROJECTS LIST HEADER ===
        header = ft.Row([
            ft.Text("PROYECTOS", size=18, weight="bold", color="white"),
            ft.Container(expand=True),
            import_btn
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Load existing projects
        self._refresh_projects_list()

        # Main content
        content = ft.Column([
            ft.Container(height=20),
            ft.Row([hero_card], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=40),
            header,
            ft.Container(height=12),
            self.projects_list,
        ], expand=True, scroll=ft.ScrollMode.AUTO)

        return ft.Container(
            padding=40,
            bgcolor="#010206",
            content=content,
            expand=True
        )

    def _refresh_projects_list(self):
        self.projects_list.controls.clear()
        projects = self.pm.get_all_projects()

        if not projects:
            self.projects_list.controls.append(
                ft.Container(
                    padding=40,
                    content=ft.Text("Aún no tienes proyectos. Crea o importa uno.", 
                                    color="#556677", size=14, italic=True)
                )
            )
            return

        for proj in projects:
            card = self._build_project_card(proj)
            self.projects_list.controls.append(card)

    def _build_project_card(self, project: dict):
        return ft.Container(
            bgcolor="#0A0B10",
            border=ft.Border(ft.BorderSide(1, "#1F2633")),
            border_radius=16,
            padding=18,
            content=ft.Row([
                ft.Image(src="/home/user/legna1/ui/svg/code_editor.svg", width=42, height=42),
                ft.Container(width=18),
                ft.Column([
                    ft.Text(project["name"], size=16, weight="bold", color="white"),
                    ft.Text(f"{project.get('file_count', 0)} archivos  •  {project.get('size_mb', 0)} MB", 
                            size=11, color="#667788"),
                    ft.Text(project.get("description", ""), size=11, color="#556677", max_lines=1)
                ], spacing=3, expand=True),
                ft.Column([
                    ft.Text(project.get("created_at", "")[:10], size=10, color="#556677"),
                    ft.Container(height=8),
                    ft.ElevatedButton(
                        "Abrir",
                        style=ft.ButtonStyle(
                            bgcolor="#00D9FF20",
                            color="#00D9FF",
                            padding=ft.padding.symmetric(horizontal=18, vertical=6),
                            shape=ft.RoundedRectangleBorder(radius=8)
                        ),
                        on_click=lambda e, p=project: self._open_project(p)
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.END)
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def _create_new_project(self, e):
        def create_dialog_result(name):
            if name:
                proj = self.pm.create_new_project(name)
                self._refresh_projects_list()
                self.page.update()
                self._show_import_success_dialog(proj, is_new=True)

        # Simple text dialog
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Nombre del nuevo proyecto"),
            content=ft.TextField(label="Nombre del proyecto", autofocus=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self._close_dialog()),
                ft.TextButton("Crear", on_click=lambda e: create_dialog_result(self.page.dialog.content.value))
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def _import_project_dialog(self, e):
        def pick_folder(result):
            if result and result.path:
                try:
                    # Ask if user wants to move or keep original location
                    self._show_move_or_reference_dialog(result.path)
                except Exception as ex:
                    self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"))
                    self.page.snack_bar.open = True
                    self.page.update()

        # Use Flet file picker
        picker = ft.FilePicker(on_result=pick_folder)
        self.page.overlay.append(picker)
        self.page.update()
        picker.get_directory_path()

    def _show_move_or_reference_dialog(self, folder_path: str):
        def do_import(move: bool):
            try:
                proj = self.pm.import_project(folder_path, move=move)
                self._refresh_projects_list()
                self.page.update()
                self._show_import_success_dialog(proj)
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error importando: {str(ex)}"))
                self.page.snack_bar.open = True
                self.page.update()
            finally:
                self._close_dialog()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("¿Cómo quieres importar el proyecto?"),
            content=ft.Column([
                ft.Text("Elige la opción que prefieras:", size=14),
                ft.Container(height=20),
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Text("Mover a Workspace", size=13),
                        on_click=lambda e: do_import(True),
                        style=ft.ButtonStyle(bgcolor="#00D9FF", color="white")
                    ),
                    ft.ElevatedButton(
                        content=ft.Text("Dejar en ubicación original", size=13),
                        on_click=lambda e: do_import(False),
                        style=ft.ButtonStyle(bgcolor="#1A1C25", color="#00D9FF", side=ft.BorderSide(1, "#00D9FF"))
                    )
                ], spacing=15, alignment=ft.MainAxisAlignment.CENTER)
            ]),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: self._close_dialog())]
        )
        self.page.dialog.open = True
        self.page.update()

    def _show_import_success_dialog(self, project: dict, is_new: bool = False):
        title = "¡Proyecto creado!" if is_new else "¡Proyecto importado!"
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Text(title, color="#00D9FF"),
            content=ft.Column([
                ft.Text(f"Proyecto: {project['name']}", size=15, weight="bold"),
                ft.Text(f"Archivos: {project.get('file_count', 0)}", size=13),
                ft.Container(height=15),
                ft.Text("¿Quieres abrirlo ahora con el Editor de Código Legna?", size=13, color="#8899AA")
            ]),
            actions=[
                ft.TextButton("Más tarde", on_click=lambda e: self._close_dialog()),
                ft.ElevatedButton(
                    "Abrir en Editor",
                    style=ft.ButtonStyle(bgcolor="#00D9FF", color="white"),
                    on_click=lambda e: self._open_editor(project)
                )
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def _open_project(self, project: dict):
        self._open_editor(project)

    def _open_editor(self, project: dict):
        """Open the beautiful Legna Monaco Editor v3.0"""
        from ui.legna_monaco_editor import LegnaMonacoEditor
        
        editor = LegnaMonacoEditor(self.page, project)
        editor_screen = editor.build()
        editor._refresh_file_tree()
        
        self.page.controls.clear()
        self.page.add(editor_screen)
        self.page.update()

    def _close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()