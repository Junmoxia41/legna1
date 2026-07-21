import webview
import threading
import psutil
import time
import os
from assistant import LegnaAssistant

class API:
    """Clase para comunicar JavaScript con Python"""
    def __init__(self, assistant, window):
        self.assistant = assistant
        self.window = window

    def get_user_data(self):
        return self.assistant.memory_manager.database.get_full_identity()

    def process_chat(self, message):
        """Procesa un mensaje del chat y devuelve la respuesta de Legna"""
        try:
            # Procesar el mensaje con el motor de Legna
            evaluations = self.assistant.process_message(message)
            
            # Lógica simple de respuesta por ahora (se puede conectar al LLM real)
            if any(ev.memory_type == "command" for ev in evaluations):
                return "Comando ejecutado en el núcleo de Legna."
            else:
                return "Entendido. He actualizado mi base de conocimientos."
        except Exception as e:
            return f"Error en el núcleo: {str(e)}"

def update_loop(window):
    """Bucle en segundo plano para actualizar CPU/RAM"""
    while True:
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            window.evaluate_js(f"updateStats({cpu}, {ram})")
            time.sleep(2)
        except: break

def run_app():
    assistant = LegnaAssistant()
    
    # Ruta al archivo HTML
    html_path = os.path.join(os.getcwd(), "legna1", "ui", "index.html")
    if not os.path.exists(html_path):
        html_path = os.path.join(os.getcwd(), "ui", "index.html")

    # Crear Ventana Nativa con el motor PyWebView
    window = webview.create_window(
        'LEGNA | NEURAL INTERFACE OS', 
        html_path,
        width=1300, height=850,
        background_color='#010206'
    )

    # Iniciar API
    api = API(assistant, window)
    window.expose(api.process_chat, api.get_user_data)
    
    def on_loaded():
        # Poner el nombre del usuario al iniciar
        identity = assistant.memory_manager.database.get_full_identity()
        name = identity.get('nombre', 'Operador')
        window.evaluate_js(f"setUserName('{name}')")
        # Iniciar monitor
        threading.Thread(target=update_loop, args=(window,), daemon=True).start()

    webview.start(on_loaded, debug=False)

if __name__ == "__main__":
    run_app()
