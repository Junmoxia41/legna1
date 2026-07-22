"""
LegnaCode Editor - VS Code style editor for Legna v2.0
Fully integrated with Project Manager
Uses custom SVG icons (no emojis)
"""

import flet as ft
from pathlib import Path
from workspace.project_manager import ProjectManager
import os


class LegnaCodeEditor:
    def __init__(self, page: ft.Page, project: dict = None):
        self.page = page
        self.pm = ProjectManager()
        self.current_project = project
        self.current_file = None
        self.open_files = {}  # path -> content
        self.tabs = ft.Tabs(selected_index=0, on_change=self._on_tab_change)
        self.file_tree = ft.ListView(expand=True, spacing=2)
        self.editor_area = ft.TextField(
            multiline=True,
            expand=True,
            border=ft.InputBorder.NONE,
            text_style=ft.TextStyle(font_family="monospace", size=14, color="#E0E6ED"),
            bgcolor="#0A0B10",
            content_padding=20,
            on_change=self._on_content_change
        )
        self.status_bar = ft.Container(
            height=28,
            bgcolor="#05060A",
            padding=ft.padding.symmetric(horizontal=16),
            content=ft.Row([
                ft.Text("LegnaCode Editor", size=11, color="#556677"),
                ft.Container(expand=True),
                ft.Text("Python", size=11, color="#556677"),
            ])
        )

    def build(self):
        if not self.current_project:
            return ft.Container(
                content=ft.Text("No hay proyecto abierto", size=20, color="#556677"),
                alignment=ft.alignment.center,
                expand=True
            )

        # Load file tree
        self._load_file_tree()

        # Sidebar - File Explorer
        sidebar = ft.Container(
            width=260,
            bgcolor="#05060A",
            border=ft.Border(right=ft.BorderSide(1, "#1F2633")),
            padding=ft.padding.only(top=12, left=8, right=8),
            content=ft.Column([
                ft.Row([
                    ft.Image(src="/home/user/legna1/ui/svg/code_editor.svg", width=20, height=20),
                    ft.Text("EXPLORER", size=10, weight="bold", color="#667788"),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.REFRESH, icon_size=16, on_click=lambda e: self._load_file_tree())
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(color="#1F2633", height=1),
                self.file_tree
            ], expand=True)
        )

        # Main editor area with tabs
        editor_container = ft.Container(
            expand=True,
            bgcolor="#0A0B10",
            content=ft.Column([
                self.tabs,
                self.editor_area
            ], expand=True, spacing=0)
        )

        # Top bar
        top_bar = ft.Container(
            height=48,
            bgcolor="#05060A",
            padding=ft.padding.symmetric(horizontal=16),
            content=ft.Row([
                ft.Text(self.current_project["name"], size=15, weight="bold", color="#00D9FF"),
                ft.Container(expand=True),
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Row([ft.Text("Guardar", size=12)], spacing=6),
                        style=ft.ButtonStyle(bgcolor="#1A1C25", color="#00D9FF", padding=8),
                        on_click=self._save_current_file
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([ft.Text("Ejecutar", size=12)], spacing=6),
                        style=ft.ButtonStyle(bgcolor="#00D9FF", color="white", padding=8),
                        on_click=self._run_file
                    )
                ], spacing=8)
            ])
        )

        # Full layout
        layout = ft.Column([
            top_bar,
            ft.Row([
                sidebar,
                editor_container
            ], expand=True, spacing=0),
            self.status_bar
        ], expand=True, spacing=0)

        return layout

    def _load_file_tree(self):
        self.file_tree.controls.clear()
        if not self.current_project:
            return

        base_path = Path(self.current_project["path"])
        files = self.pm.scan_project_files(self.current_project["id"])

        for file_path in sorted(files):
            full_path = base_path / file_path
            is_dir = full_path.is_dir()

            item = ft.Container(
                content=ft.Row([
                    ft.Image(
                        src="/home/user/legna1/ui/svg/code_editor.svg" if not is_dir else "/home/user/legna1/ui/svg/folder_plus.svg",
                        width=16, height=16
                    ) if not is_dir else ft.Icon(ft.Icons.FOLDER, size=16, color="#00D9FF"),
                    ft.Text(file_path, size=12, color="#E0E6ED", expand=True)
                ], spacing=8),
                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                border_radius=6,
                on_click=lambda e, p=str(full_path): self._open_file(p)
            )
            self.file_tree.controls.append(item)

        self.page.update()

    def _open_file(self, file_path: str):
        path = Path(file_path)
        if not path.is_file():
            return

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except:
            content = "# Error al leer el archivo"

        self.current_file = str(path)
        self.open_files[str(path)] = content

        # Update tabs
        self._update_tabs()

        # Load content
        self.editor_area.value = content
        self.editor_area.update()

        # Update status
        self.status_bar.content.controls[2].value = path.suffix.upper().replace(".", "") or "TXT"
        self.status_bar.update()

    def _update_tabs(self):
        self.tabs.tabs.clear()
        for path in self.open_files.keys():
            name = Path(path).name
            self.tabs.tabs.append(
                ft.Tab(
                    text=name,
                    icon=ft.Icons.DESCRIPTION,
                    content=ft.Container()
                )
            )
        if self.tabs.tabs:
            self.tabs.selected_index = len(self.tabs.tabs) - 1
        self.tabs.update()

    def _on_tab_change(self, e):
        if self.tabs.selected_index is not None and self.open_files:
            paths = list(self.open_files.keys())
            if self.tabs.selected_index < len(paths):
                selected_path = paths[self.tabs.selected_index]
                self.current_file = selected_path
                self.editor_area.value = self.open_files[selected_path]
                self.editor_area.update()

    def _on_content_change(self, e):
        if self.current_file:
            self.open_files[self.current_file] = self.editor_area.value

    def _save_current_file(self, e):
        if not self.current_file:
            return

        try:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.editor_area.value)
            self.page.snack_bar = ft.SnackBar(ft.Text("Archivo guardado ✓", color="#00D9FF"))
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def _run_file(self, e):
        if not self.current_file:
            return
        self.page.snack_bar = ft.SnackBar(
            ft.Text(f"Ejecutando {Path(self.current_file).name} (próximamente con terminal integrada)", color="#00D9FF")
        )
        self.page.snack_bar.open = True
        self.page.update()

    def open_project(self, project: dict):
        """Public method to open a project in the editor"""
        self.current_project = project
        self.open_files = {}
        self.current_file = None
        self.editor_area.value = ""
        self._load_file_tree()
        self.page.update()