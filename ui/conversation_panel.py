"""
Conversation Panel - Right sidebar for Chat section
Shows saved conversations (as neurons) + "Nueva Conversación" button
Replaces "CORE_ACTIVE" when entering chat
"""

import flet as ft
from datetime import datetime
from memory.conversation_manager import ConversationManager


class ConversationPanel:
    def __init__(self, page: ft.Page, on_new_chat=None, on_open_chat=None):
        self.page = page
        self.on_new_chat = on_new_chat
        self.on_open_chat = on_open_chat
        self.conversation_manager = ConversationManager()
        self.conversations = self.conversation_manager.get_all_conversations()

    def _load_sample_conversations(self):
        """Temporary sample data - later will come from memory"""
        return [
            {
                "id": "conv_001",
                "title": "Análisis de proyecto legna1",
                "last_message": "Vamos a modificar el archivo main.py",
                "date": "2026-07-21 14:32",
                "message_count": 12
            },
            {
                "id": "conv_002",
                "title": "Importar nuevo proyecto",
                "last_message": "¿Quieres que lo mueva a workspace?",
                "date": "2026-07-20 19:45",
                "message_count": 7
            },
            {
                "id": "conv_003",
                "title": "Configuración de memoria neuronal",
                "last_message": "Recuerda mi segundo nombre: Yolexis",
                "date": "2026-07-19 11:10",
                "message_count": 23
            }
        ]

    def build(self):
        header = ft.Row([
            ft.Text("CONVERSACIONES", size=11, weight="bold", color="#667788"),
            ft.Container(expand=True),
            ft.IconButton(
                icon=ft.Icons.ADD,
                icon_color="#00D9FF",
                icon_size=20,
                tooltip="Nueva Conversación",
                on_click=self._new_conversation
            )
        ])

        conv_list = ft.ListView(expand=True, spacing=6, padding=ft.padding.only(top=12))

        for conv in self.conversations:
            card = self._build_conversation_card(conv)
            conv_list.controls.append(card)

        # Big "Nueva Conversación" button
        new_chat_btn = ft.ElevatedButton(
            content=ft.Row([
                ft.Image(src="/home/user/legna1/ui/svg/new_chat.svg", width=26, height=26),
                ft.Container(width=10),
                ft.Text("NUEVA CONVERSACIÓN", size=13, weight="bold")
            ], alignment=ft.MainAxisAlignment.CENTER),
            style=ft.ButtonStyle(
                bgcolor="#00D9FF",
                color="white",
                padding=ft.padding.symmetric(horizontal=24, vertical=14),
                shape=ft.RoundedRectangleBorder(radius=12)
            ),
            on_click=self._new_conversation
        )

        return ft.Container(
            width=300,
            bgcolor="#05060A",
            padding=ft.padding.all(20),
            border=ft.Border(left=ft.BorderSide(1, "#1F2633")),
            content=ft.Column([
                header,
                ft.Container(height=8),
                conv_list,
                ft.Container(height=20),
                new_chat_btn
            ], expand=True)
        )

    def refresh(self):
        """Refresh the list with latest conversations"""
        self.conversations = self.conversation_manager.get_all_conversations()
        # Note: In a real implementation, we would rebuild the UI here
        # For now, the panel will refresh on next chat navigation

    def _build_conversation_card(self, conv: dict):
        # Handle both old sample format and new persisted format
        title = conv.get("title", "Conversación")
        count = conv.get("message_count", 0)
        last_msg = conv.get("last_message", conv.get("context_summary", "Sin mensajes aún"))
        date = conv.get("date", conv.get("last_updated", "")[:16].replace("T", " "))
        
        return ft.Container(
            bgcolor="#0A0B10",
            border=ft.Border(ft.BorderSide(1, "#1F2633")),
            border_radius=12,
            padding=14,
            on_click=lambda e: self._open_conversation(conv),
            content=ft.Column([
                ft.Row([
                    ft.Text(title, size=13, weight="bold", color="white", expand=True),
                    ft.Text(str(count), size=10, color="#556677")
                ]),
                ft.Container(height=4),
                ft.Text(last_msg[:60] + ("..." if len(str(last_msg)) > 60 else ""), 
                        size=11, color="#8899AA", max_lines=2),
                ft.Container(height=6),
                ft.Text(date, size=9, color="#556677")
            ])
        )

    def _new_conversation(self, e):
        if self.on_new_chat:
            self.on_new_chat()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Nueva conversación iniciada ✓"))
            self.page.snack_bar.open = True
            self.page.update()

    def _open_conversation(self, conv: dict):
        if self.on_open_chat:
            self.on_open_chat(conv)
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Abrir: {conv['title']}"))
            self.page.snack_bar.open = True
            self.page.update()