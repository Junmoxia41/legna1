import flet as ft
import asyncio
from ui.styles import *

class SplashScreen:
    def __init__(self, on_complete):
        self.on_complete = on_complete
        self.logo = ft.Text("L", size=85, weight="bold", font_family="SpaceGrotesk", color=C_CYAN)
        self.logo_container = ft.Container(content=self.logo, animate_scale=1000, scale=1.0)
        self.progress_bar = ft.ProgressBar(width=450, color=C_CYAN, bgcolor="#111218", value=0)
        self.status_msg = ft.Text("INITIALIZING NEURAL INTERFACE...", style=S_HUD, size=12)

    def build(self):
        # ELIMINADO letter_spacing que causaba el TypeError
        content = ft.Column([
            self.logo_container,
            ft.Text("LEGNA", size=35, weight="bold", color="white"),
            ft.Container(height=50),
            self.status_msg,
            self.progress_bar
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
        
        return ft.Container(content=content, expand=True, alignment=ft.Alignment(0, 0), bgcolor="black")

    async def animate(self, page):
        await asyncio.sleep(0.5)
        for i in range(101):
            self.progress_bar.value = i / 100
            if i % 20 == 0:
                self.logo_container.scale = 1.1 if self.logo_container.scale == 1.0 else 1.0
            page.update()
            await asyncio.sleep(0.06)
        await asyncio.sleep(0.5)
        self.on_complete()
