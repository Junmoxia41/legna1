"""
Real Terminal Integration - Legna v2.0
Executes real system commands and shows live output
"""

import flet as ft
import subprocess
import threading
import os
from pathlib import Path


class RealTerminal:
    def __init__(self, page: ft.Page, working_dir: str = None):
        self.page = page
        self.working_dir = working_dir or os.getcwd()
        self.output = ft.TextField(
            multiline=True,
            read_only=True,
            expand=True,
            border=ft.InputBorder.NONE,
            text_style=ft.TextStyle(font_family="monospace", size=13, color="#00FF9F"),
            bgcolor="#05060A",
            value="Legna Terminal v2.1 (Real)\n> "
        )
        self.input = ft.TextField(
            hint_text="Escribe un comando real...",
            border=ft.InputBorder.NONE,
            on_submit=self._run_real_command,
            text_style=ft.TextStyle(font_family="monospace", size=13)
        )

    def build(self):
        return ft.Container(
            height=200,
            bgcolor="#05060A",
            border=ft.Border(top=ft.BorderSide(1, "#1F2633")),
            padding=ft.padding.all(10),
            content=ft.Column([
                ft.Row([
                    ft.Text("TERMINAL REAL", size=10, weight="bold", color="#667788"),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.CLEAR, icon_size=14, on_click=self._clear)
                ]),
                self.output,
                self.input
            ], spacing=6, expand=True)
        )

    def _run_real_command(self, e):
        cmd = self.input.value.strip()
        if not cmd:
            return

        self._append(f"\n> {cmd}\n")
        self.input.value = ""

        # Run in background thread
        threading.Thread(target=self._execute_command, args=(cmd,), daemon=True).start()
        self.page.update()

    def _execute_command(self, cmd: str):
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout or result.stderr or "(sin salida)"
            self._append(output + "\n")
            
        except subprocess.TimeoutExpired:
            self._append("⏱️ Comando cancelado por timeout (30s)\n")
        except Exception as ex:
            self._append(f"❌ Error: {str(ex)}\n")

        self.page.update()

    def _append(self, text: str):
        self.output.value += text
        self.page.update()

    def _clear(self, e):
        self.output.value = "Legna Terminal v2.1 (Real)\n> "
        self.page.update()

    def set_working_directory(self, path: str):
        self.working_dir = path
        self._append(f"\n📁 Directorio cambiado a: {path}\n")