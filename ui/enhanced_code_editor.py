"""
Enhanced LegnaCode Editor v2.2
- Real terminal execution
- Monaco Editor ready
- Better UX
"""

import flet as ft
import threading
from pathlib import Path
from workspace.project_manager import ProjectManager
from ui.real_terminal import RealTerminal


class EnhancedLegnaCodeEditor:
    def __init__(self, page: ft.Page, project: dict = None):
        self.page = page
        self.pm = ProjectManager()
        self.current_project = project
        self.current_file = None
        self.open_files = {}           # path -> {content, modified}
        self.file_tree = ft.ListView(expand=True, spacing=1)
        
        # Main editor
        self.editor = ft.TextField(
            multiline=True,
            expand=True,
            border=ft.InputBorder.NONE,
            text_style=ft.TextStyle(font_family="monospace", size=14, color="#E0E6ED"),
            bgcolor="#0A0B10",
            content_padding=20,
            on_change=self._mark_modified
        )
        
        self.tabs = ft.Tabs(selected_index=0, on_change=self._on_tab_change, height=42)
        
        # Real Terminal
        working_dir = str(Path(project["path"])) if project else None
        self.real_terminal = RealTerminal(page, working_dir)
        
        self.status_bar = ft.Container(
            height=26,
            bgcolor="#05060A",
            padding=ft.padding.symmetric(horizontal=16),
            content=ft.Row([
                ft.Text("LegnaCode v2.2", size=11, color="#556677"),
                ft.Container(expand=True),
                ft.Text("Python", size=11, color="#00D9FF"),
                ft.Container(width=20),
                ft.Text("Ln 1, Col 1", size=11, color="#556677"),
            ])
        )

    def build(self):
        if not self.current_project:
            return ft.Container(
                content=ft.Text("No hay proyecto abierto", size=20, color="#556677"),
                alignment=ft.alignment.center, expand=True
            )

        # Sidebar
        sidebar = ft.Container(
            width=250,
            bgcolor="#05060A",
            border=ft.Border(right=ft.BorderSide(1, "#1F2633")),
            padding=ft.padding.only(top=10, left=6, right=6),
            content=ft.Column([
                ft.Row([
                    ft.Text("EXPLORER", size=10, weight="bold", color="#667788"),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.REFRESH, icon_size=16, on_click=lambda e: self._load_file_tree())
                ]),
                ft.Divider(color="#1F2633", height=1),
                self.file_tree
            ], expand=True)
        )

        # Editor area with tabs
        editor_area = ft.Container(
            expand=True,
            bgcolor="#0A0B10",
            content=ft.Column([
                self.tabs,
                self.editor
            ], spacing=0, expand=True)
        )

        # Top bar
        top_bar = ft.Container(
            height=46,
            bgcolor="#05060A",
            padding=ft.padding.symmetric(horizontal=16),
            content=ft.Row([
                ft.Text(self.current_project["name"], size=15, weight="bold", color="#00D9FF"),
                ft.Container(expand=True),
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Text("Guardar", size=12),
                        style=ft.ButtonStyle(bgcolor="#1A1C25", color="#00D9FF", padding=8),
                        on_click=self._save_current_file
                    ),
                    ft.ElevatedButton(
                        content=ft.Text("Ejecutar", size=12),
                        style=ft.ButtonStyle(bgcolor="#00D9FF", color="white", padding=8),
                        on_click=self._run_current_file
                    ),
                    ft.ElevatedButton(
                        content=ft.Text("Monaco", size=12),
                        style=ft.ButtonStyle(bgcolor="#6A5CFF", color="white", padding=8),
                        on_click=self._open_monaco_editor
                    )
                ], spacing=8)
            ])
        )

        # Main layout with Real Terminal
        return ft.Column([
            top_bar,
            ft.Row([sidebar, editor_area], expand=True, spacing=0),
            self.real_terminal.build(),
            self.status_bar
        ], expand=True, spacing=0)

    def _load_file_tree(self):
        self.file_tree.controls.clear()
        if not self.current_project:
            return

        base = Path(self.current_project["path"])
        files = self.pm.scan_project_files(self.current_project["id"])

        for file_path in sorted(files)[:40]:  # Limit for performance
            full_path = str(base / file_path)
            is_dir = (base / file_path).is_dir()

            row = ft.Row([
                ft.Image(
                    src="/home/user/legna1/ui/svg/code_editor.svg",
                    width=15, height=15
                ) if not is_dir else ft.Icon(ft.Icons.FOLDER_OPEN, size=15, color="#00D9FF"),
                ft.Text(file_path, size=11, color="#E0E6ED", expand=True)
            ], spacing=6)

            item = ft.Container(
                content=row,
                padding=ft.padding.symmetric(horizontal=8, vertical=3),
                border_radius=4,
                on_click=lambda e, p=full_path: self._open_file(p)
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
        self.open_files[str(path)] = {"content": content, "modified": False}

        self._update_tabs()
        self.editor.value = content
        self.editor.update()

        # Update status
        ext = path.suffix.upper().replace(".", "") or "TXT"
        self.status_bar.content.controls[2].value = ext
        self.status_bar.update()

    def _update_tabs(self):
        self.tabs.tabs.clear()
        for path_str, data in self.open_files.items():
            name = Path(path_str).name
            modified = " •" if data.get("modified") else ""
            self.tabs.tabs.append(ft.Tab(text=name + modified, icon=ft.Icons.DESCRIPTION))
        
        if self.tabs.tabs:
            self.tabs.selected_index = len(self.tabs.tabs) - 1
        self.tabs.update()

    def _on_tab_change(self, e):
        if self.tabs.selected_index is not None and self.open_files:
            paths = list(self.open_files.keys())
            if self.tabs.selected_index < len(paths):
                selected = paths[self.tabs.selected_index]
                self.current_file = selected
                self.editor.value = self.open_files[selected]["content"]
                self.editor.update()

    def _mark_modified(self, e):
        if self.current_file and self.current_file in self.open_files:
            self.open_files[self.current_file]["content"] = self.editor.value
            self.open_files[self.current_file]["modified"] = True
            self._update_tabs()

    def _save_current_file(self, e):
        if not self.current_file:
            return

        try:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.editor.value)
            
            self.open_files[self.current_file]["modified"] = False
            self._update_tabs()
            
            self.page.snack_bar = ft.SnackBar(ft.Text("✓ Archivo guardado", color="#00D9FF"))
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def _run_current_file(self, e):
        if not self.current_file:
            return
        
        cmd = f"python \"{self.current_file}\""
        self.real_terminal._append(f"\n> Ejecutando: {Path(self.current_file).name}\n")
        # Execute via real terminal
        threading.Thread(
            target=self.real_terminal._execute_command, 
            args=(cmd,), 
            daemon=True
        ).start()

    def _execute_terminal_command(self, e):
        cmd = self.terminal_input.value.strip()
        if not cmd:
            return
        
        self._append_to_terminal(f"\n> {cmd}\n")
        
        # Simple command simulation
        if cmd == "ls":
            self._append_to_terminal("src/  docs/  main.py  README.md\n")
        elif cmd == "clear":
            self.terminal_output.value = "Legna Terminal v2.1\n"
        else:
            self._append_to_terminal(f"Comando ejecutado: {cmd}\n")
        
        self.terminal_input.value = ""
        self.terminal_output.update()
        self.terminal_input.update()

    def _append_to_terminal(self, text: str):
        self.terminal_output.value += text
        self.terminal_output.update()

    def _open_monaco_editor(self, e):
        """Open Monaco Editor in a new view"""
        from ui.monaco_webview import MonacoWebView
        
        if self.current_file:
            with open(self.current_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        else:
            content = "# Abre un archivo para editarlo con Monaco"
        
        monaco_view = MonacoWebView(self.page, self.current_file, content)
        self.page.controls.clear()
        self.page.add(monaco_view.build())
        self.page.update()

    def open_project(self, project: dict):
        self.current_project = project
        self.open_files = {}
        self.current_file = None
        self.editor.value = ""
        self._load_file_tree()
        self.page.update()