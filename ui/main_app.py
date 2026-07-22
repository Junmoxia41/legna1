"""
Legna v2.0 - Main Application Entry
Full navigation with:
- Dashboard
- Workspace (big card + import + editor)
- Chat (with dynamic conversation panel + human greetings)
Uses custom SVG icons (no emojis)
"""

import flet as ft
from ui.dashboard import DashboardScreen
from ui.workspace_view import WorkspaceScreen
from ui.chat_screen import ChatScreen
from ui.memory_brain_view import MemoryBrainView


def main(page: ft.Page):
    page.title = "LEGNA v2.0 - Neural Interface"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#010206"
    page.padding = 0
    page.window_width = 1400
    page.window_height = 860

    # Current active screen container
    current_screen = ft.Container(expand=True)

    def switch_screen(screen_name: str):
        if screen_name == "dashboard":
            screen = DashboardScreen(None).build()
        elif screen_name == "workspace":
            screen = WorkspaceScreen(page).build()
        elif screen_name == "chat":
            screen = ChatScreen(page).build()
        elif screen_name == "memory":
            screen = MemoryBrainView(page).build()
        else:
            screen = ft.Container(
                content=ft.Column([
                    ft.Image(src="/home/user/legna1/ui/svg/brain.svg", width=80, height=80),
                    ft.Text(f"Sección {screen_name.upper()} en desarrollo", 
                            size=22, color="#556677", weight="bold")
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                expand=True
            )

        current_screen.content = screen
        page.update()

    # Enhanced Sidebar with custom SVGs
    def nav_item(icon_path, label, screen_name, active=False):
        return ft.Container(
            content=ft.Row([
                ft.Image(src=icon_path, width=22, height=22),
                ft.Text(label, size=13, weight="bold" if active else "normal", 
                        color="#00D9FF" if active else "#808590")
            ], spacing=14),
            padding=ft.padding.symmetric(horizontal=18, vertical=13),
            border_radius=10,
            bgcolor="#151820" if active else "transparent",
            on_click=lambda e: switch_screen(screen_name)
        )

    sidebar = ft.Container(
        width=245,
        bgcolor="#05060A",
        padding=ft.padding.only(top=32, left=22, right=22, bottom=32),
        border=ft.Border(right=ft.BorderSide(1, "#1F2633")),
        content=ft.Column([
            ft.Row([
                ft.Image(src="/home/user/legna1/ui/svg/folder_plus.svg", width=34, height=34),
                ft.Text("LEGNA", size=26, weight="bold", color="#00D9FF")
            ], spacing=12),
            ft.Text("NEURAL INTERFACE v2.0", size=9, color="#404550", letter_spacing=2.5),
            ft.Container(height=42),
            
            nav_item("/home/user/legna1/ui/svg/folder_plus.svg", "DASHBOARD", "dashboard", True),
            nav_item("/home/user/legna1/ui/svg/code_editor.svg", "WORKSPACE", "workspace"),
            nav_item("/home/user/legna1/ui/svg/conversations.svg", "CHAT", "chat"),
            nav_item("/home/user/legna1/ui/svg/brain.svg", "MEMORIA", "memory"),
            
            ft.Container(expand=True),
            ft.Divider(color="#1F2633"),
            ft.Container(height=14),
            ft.Row([
                ft.CircleAvatar(content=ft.Text("A", color="white", size=14), bgcolor="#00D9FF", radius=14),
                ft.Column([
                    ft.Text("Airien Yolexis", size=12, weight="bold", color="white"),
                    ft.Text("USUARIO PREMIUM", size=9, color="#00D9FF")
                ], spacing=1)
            ], spacing=12)
        ])
    )

    # Main layout
    layout = ft.Row([
        sidebar,
        current_screen
    ], expand=True, spacing=0)

    # Initial screen: Dashboard
    current_screen.content = DashboardScreen(None).build()

    page.add(layout)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)