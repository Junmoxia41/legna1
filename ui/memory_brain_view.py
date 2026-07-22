"""
Memory Brain View - Legna v2.0
Neural Memory Interface
Brain SVG + Memory Cards (categorized neural memories)
"""

import flet as ft
from datetime import datetime
from memory.neural_memory import NeuralMemoryManager


class MemoryBrainView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.neural_memory = NeuralMemoryManager()
        self.memories = self.neural_memory.get_all_memories()

    def _load_sample_memories(self):
        """Sample neural memories - will be replaced with real DB"""
        return [
            {"category": "nombre", "key": "nombre", "value": "Airien", "confidence": 0.98, "date": "2026-07-10"},
            {"category": "nombre", "key": "segundo_nombre", "value": "Yolexis", "confidence": 0.95, "date": "2026-07-10"},
            {"category": "edad", "key": "edad", "value": "19", "confidence": 0.92, "date": "2026-07-12"},
            {"category": "comando", "key": "ipconfig", "value": "Muestra configuración de red", "confidence": 0.85, "date": "2026-07-18"},
            {"category": "preferencia", "key": "color_favorito", "value": "cyan", "confidence": 0.78, "date": "2026-07-15"},
            {"category": "proyecto", "key": "legna1", "value": "Proyecto principal de Legna", "confidence": 0.90, "date": "2026-07-20"},
        ]

    def build(self):
        # Reload memories from disk
        self.memories = self.neural_memory.get_all_memories()

        # Big Brain Header
        brain_header = ft.Container(
            height=180,
            alignment=ft.alignment.center,
            content=ft.Column([
                ft.Image(src="/home/user/legna1/ui/svg/brain.svg", width=110, height=110),
                ft.Text("CEREBRO DE LEGNA", size=22, weight="bold", color="#00D9FF"),
                ft.Text("Memoria Neuronal • Recuerdos Categorizados", size=12, color="#667788")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8)
        )

        # Memory Cards Grid
        cards_row = ft.Row(wrap=True, spacing=16, run_spacing=16, expand=True)

        if not self.memories:
            cards_row.controls.append(
                ft.Container(
                    content=ft.Text("Aún no hay recuerdos neuronales.\nHabla conmigo en el chat para que empiece a aprender.", 
                                    size=14, color="#667788", text_align=ft.TextAlign.CENTER),
                    padding=40
                )
            )
        else:
            for mem in self.memories:
                card = self._create_memory_card(mem)
                cards_row.controls.append(card)

        # Add new memory button
        add_btn = ft.ElevatedButton(
            content=ft.Row([
                ft.Text("+ AÑADIR RECUERDO", size=13, weight="bold")
            ]),
            style=ft.ButtonStyle(
                bgcolor="#1A1C25",
                color="#00D9FF",
                padding=ft.padding.symmetric(horizontal=28, vertical=12),
                shape=ft.RoundedRectangleBorder(radius=12)
            ),
            on_click=self._add_memory_dialog
        )

        return ft.Container(
            padding=40,
            bgcolor="#010206",
            expand=True,
            content=ft.Column([
                brain_header,
                ft.Container(height=20),
                ft.Row([
                    ft.Text("RECuerdos NEURONALES", size=16, weight="bold", color="white"),
                    ft.Container(expand=True),
                    add_btn
                ]),
                ft.Container(height=16),
                cards_row
            ], expand=True, scroll=ft.ScrollMode.AUTO)
        )

    def _create_memory_card(self, memory: dict):
        category_color = {
            "nombre": "#00D9FF",
            "edad": "#6A5CFF",
            "comando": "#FFB300",
            "preferencia": "#00FF9F",
            "proyecto": "#FF6B6B"
        }.get(memory["category"], "#00D9FF")

        return ft.Container(
            width=260,
            height=160,
            bgcolor="#0A0B10",
            border=ft.Border(ft.BorderSide(1.5, category_color)),
            border_radius=18,
            padding=18,
            on_click=lambda e: self._show_memory_detail(memory),
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        width=8, height=8,
                        bgcolor=category_color,
                        border_radius=4
                    ),
                    ft.Text(memory["category"].upper(), size=10, weight="bold", color=category_color),
                    ft.Container(expand=True),
                    ft.Text(f"{int(memory['confidence']*100)}%", size=10, color="#556677")
                ]),
                ft.Container(height=12),
                ft.Text(memory["key"], size=13, color="#8899AA"),
                ft.Text(memory["value"], size=16, weight="bold", color="white", max_lines=2),
                ft.Container(height=12),
                ft.Text(memory["date"], size=10, color="#556677")
            ])
        )

    def _show_memory_detail(self, memory: dict):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text(f"Recuerdo: {memory['key']}", color="#00D9FF"),
            content=ft.Column([
                ft.Text(f"Categoría: {memory['category']}", size=13),
                ft.Text(f"Valor: {memory['value']}", size=15, weight="bold"),
                ft.Text(f"Confianza: {int(memory['confidence']*100)}%", size=12),
                ft.Text(f"Fecha: {memory['date']}", size=11, color="#667788")
            ], spacing=10),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self._close_dialog()),
                ft.TextButton("Editar", on_click=lambda e: self._edit_memory(memory))
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def _add_memory_dialog(self, e):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Nuevo Recuerdo Neuronal"),
            content=ft.Column([
                ft.TextField(label="Categoría", hint_text="nombre, edad, comando..."),
                ft.TextField(label="Clave"),
                ft.TextField(label="Valor"),
            ], spacing=12),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self._close_dialog()),
                ft.ElevatedButton("Guardar", on_click=self._save_new_memory)
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def _save_new_memory(self, e):
        # Placeholder - in real version this would save to memory manager
        self._close_dialog()
        self.page.snack_bar = ft.SnackBar(ft.Text("Recuerdo guardado en el cerebro ✓", color="#00D9FF"))
        self.page.snack_bar.open = True
        self.page.update()

    def _edit_memory(self, memory: dict):
        self._close_dialog()
        # TODO: Implement edit flow
        self.page.snack_bar = ft.SnackBar(ft.Text("Función de edición próximamente"))
        self.page.snack_bar.open = True
        self.page.update()

    def _close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()