import flet as ft
from ui.styles import *

class AuthScreen:
    def __init__(self, assistant, on_success):
        self.assistant = assistant
        self.on_success = on_success
        
        self.f_name = ft.TextField(label="Nombre", border_color=C_CYAN)
        self.surname = ft.TextField(label="Apellidos", border_color=C_CYAN)
        self.age = ft.TextField(label="Edad", border_color=C_CYAN)
        
        self.day = ft.Dropdown(label="Día", options=[ft.dropdown.Option(str(i)) for i in range(1,32)], expand=1)
        self.month = ft.Dropdown(label="Mes", options=[ft.dropdown.Option(str(i)) for i in range(1,13)], expand=1)
        self.year = ft.Dropdown(label="Año", options=[ft.dropdown.Option(str(i)) for i in range(1950,2027)], expand=2)

    def save_and_continue(self, e):
        if not self.f_name.value: 
            self.f_name.error_text = "Requerido"
            self.f_name.update()
            return
        data = {
            "nombre": self.f_name.value,
            "apellidos": self.surname.value,
            "edad": self.age.value,
            "nacimiento": f"{self.day.value}/{self.month.value}/{self.year.value}"
        }
        for k, v in data.items():
            self.assistant.memory_manager.database.save_identity_data(k, v)
        self.on_success()

    def build(self):
        form = ft.Column([
            ft.Text("USER IDENTIFICATION", style=S_HEADER, size=24),
            self.f_name, self.surname, self.age,
            ft.Row([self.day, self.month, self.year]),
            ft.Container(height=20),
            ft.FilledButton("INITIALIZE NEURAL LINK", on_click=self.save_and_continue, bgcolor=C_CYAN, color="black")
        ], width=500, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        return ft.Container(content=form, expand=True, alignment=ft.Alignment(0, 0), bgcolor=C_BG)
