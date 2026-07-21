import flet as ft
import psutil
import threading
import time
from ui.styles import *

class DashboardScreen:
    def __init__(self, assistant):
        self.assistant = assistant
        self.cpu_val = ft.Text("0%", color=C_CYAN, weight="bold", size=12)
        self.ram_val = ft.Text("0%", color=C_BLUE, weight="bold", size=12)
        
    def build(self):
        identity = self.assistant.memory_manager.database.get_full_identity()
        user_name = identity.get('nombre', 'Operador').upper()

        # 1. SIDEBAR IZQUIERDA (PREMIUM)
        sidebar = ft.Container(
            width=240, bgcolor=C_SIDEBAR, padding=25,
            border=ft.Border(right=ft.BorderSide(1, C_BORDER)),
            content=ft.Column([
                ft.Row([ft.Icon("ac_unit", color=C_CYAN, size=28), ft.Text("LEGNA", size=22, weight="bold", color="white")], spacing=10),
                ft.Text("NEURAL INTERFACE", size=9, color="#404550", letter_spacing=2),
                ft.Container(height=30),
                self.nav_item("dashboard", "DASHBOARD", True),
                self.nav_item("chat", "CHAT", False),
                self.nav_item("folder", "WORKSPACE", False),
                self.nav_item("psychology", "MEMORIA", False),
                self.nav_item("smart_toy", "AGENTES", False),
                self.nav_item("terminal", "TERMINAL", False),
                ft.Container(expand=True),
                ft.Divider(color=C_BORDER),
                ft.Row([ft.CircleAvatar(content=ft.Text(user_name[0])), ft.Column([ft.Text(user_name, size=11, weight="bold"), ft.Text("USUARIO PREMIUM", size=8, color=C_CYAN)], spacing=0)])
            ], spacing=5)
        )

        # 2. PANEL CENTRAL (DASHBOARD + CHAT RÁPIDO)
        center_panel = ft.Container(
            expand=True, padding=40, bgcolor=C_BG,
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text(f"Hola {user_name}, soy LEGNA.", style=S_HEADER, size=35),
                        ft.Text("Tu asistente de inteligencia artificial avanzada.", size=14, color="#606570"),
                    ]),
                    ft.Container(expand=True),
                    ft.Icon("notifications_outlined", color="#505560")
                ]),
                ft.Container(height=30),
                # Tarjetas Rápidas
                ft.Row([
                    self.card("Analizar archivos", "folder_open", C_CYAN),
                    self.card("Generar código", "code", C_PURPLE),
                    self.card("Crear imagen", "image", "amber"),
                ], spacing=20),
                ft.Container(height=40),
                # Chat Reciente (Para llenar espacio)
                ft.Text("CONVERSACIONES RECIENTES", style=S_HUD, size=11),
                ft.Container(
                    content=ft.ListView(expand=True, spacing=10, controls=[
                        ft.ListTile(leading=ft.Icon("chat_bubble_outline", color=C_CYAN), title=ft.Text("Optimización de Scripts Python"), subtitle=ft.Text("Hoy, 15:42"), trailing=ft.Icon("chevron_right")),
                        ft.ListTile(leading=ft.Icon("psychology", color=C_PURPLE), title=ft.Text("Análisis de Base de Datos"), subtitle=ft.Text("Ayer, 22:15"), trailing=ft.Icon("chevron_right")),
                    ]),
                    expand=True
                )
            ])
        )

        # 3. PANEL DERECHO (MONITOR DE SISTEMA)
        right_panel = ft.Container(
            width=300, bgcolor=C_SIDEBAR, padding=25,
            border=ft.Border(left=ft.BorderSide(1, C_BORDER)),
            content=ft.Column([
                ft.Text("ESTADO DEL SISTEMA", style=S_HUD),
                ft.Container(
                    content=ft.Column([
                        self.stat_row("CPU", self.cpu_val, 0.4, C_CYAN),
                        self.stat_row("RAM", self.ram_val, 0.6, C_BLUE),
                        self.stat_row("GPU", ft.Text("18%", size=12, weight="bold"), 0.18, C_PURPLE),
                    ], spacing=20),
                    padding=ft.padding.symmetric(vertical=20)
                ),
                ft.Divider(color=C_BORDER),
                ft.Text("AGENTES ACTIVOS", style=S_HUD),
                ft.Column([
                    self.agent_item("Code Agent", True),
                    self.agent_item("Search Agent", True),
                    self.agent_item("Memory Agent", False),
                ], spacing=10)
            ])
        )

        # Iniciar hilos
        threading.Thread(target=self.update_stats, daemon=True).start()
        
        return ft.Row([sidebar, center_panel, right_panel], expand=True, spacing=0)

    def nav_item(self, icon, label, active):
        return ft.Container(
            content=ft.Row([ft.Icon(icon, color=C_CYAN if active else "#505560", size=20), ft.Text(label, color="white" if active else "#808590", size=12, weight="bold" if active else "normal")], spacing=15),
            padding=12, border_radius=10, bgcolor="#151820" if active else "transparent"
        )

    def card(self, title, icon, color):
        return ft.Container(
            content=ft.Column([ft.Icon(icon, color=color, size=30), ft.Text(title, size=12, weight="bold")], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=C_GLASS, padding=20, border_radius=15, expand=1, border=ft.Border(ft.BorderSide(1, C_BORDER), ft.BorderSide(1, C_BORDER), ft.BorderSide(1, C_BORDER), ft.BorderSide(1, C_BORDER))
        )

    def stat_row(self, label, val_control, progress, color):
        return ft.Column([
            ft.Row([ft.Text(label, size=11), val_control], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.ProgressBar(value=progress, color=color, bgcolor="#1A1C25", height=4)
        ], spacing=5)

    def agent_item(self, name, active):
        return ft.Row([
            ft.Container(width=8, height=8, bgcolor="#00FF41" if active else "#505560", border_radius=5),
            ft.Text(name, size=12, color=C_TEXT),
            ft.Container(expand=True),
            ft.Text("ONLINE" if active else "OFFLINE", size=9, color="#404550")
        ])

    def update_stats(self):
        while True:
            try:
                self.cpu_val.value = f"{psutil.cpu_percent()}%"
                self.ram_val.value = f"{psutil.virtual_memory().percent}%"
                try: self.cpu_val.update(); self.ram_val.update()
                except: pass
                time.sleep(2)
            except: break
