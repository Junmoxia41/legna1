from assistant import LegnaAssistant
from commands.base import Command

# Simulamos un sistema externo que interactúa con Legna
def external_system_demo():
    print("========== LEGNA ASSISTANT DEMO ==========\n")
    
    # 1. Instanciar el asistente
    legna = LegnaAssistant()
    
    # 2. Mostrar comandos iniciales
    print("Comandos disponibles:", legna.get_available_commands())
    
    # 3. Enviar una orden (simulando input de otro sistema)
    print("\n[Sistema Externo] Enviando: 'abre el navegador'")
    legna.process_message("abre el navegador")
    
    # 4. Escalar: Añadir un comando dinámicamente
    class LightCommand(Command):
        def __init__(self):
            super().__init__(name="enciende", description="Enciende luces o dispositivos")
        def execute(self, params):
            return f"Luz encendida en: {params}"

    print("\n[Sistema Externo] Registrando nuevo comando: 'enciende'")
    legna.add_command(LightCommand())
    
    # Actualizar patrones de lenguaje para el nuevo comando (opcional, pero recomendado para el detector)
    # En un sistema real, el Detector de Comandos podría ser más inteligente (LLM) o tener una lista dinámica.
    # Por ahora, usamos los patrones en language.py.
    
    print("Comandos disponibles ahora:", legna.get_available_commands())
    
    # 5. Ejecutar el nuevo comando
    print("\n[Sistema Externo] Enviando: 'enciende el salón'")
    # Nota: El detector actual usa COMMAND_PATTERNS. 
    # Para que funcione automáticamente, 'enciende' debería estar en language.py
    # Como es un demo, lo forzamos o mostramos cómo el detector lo encontraría si estuviera en la lista.
    legna.process_message("enciende el salón")

if __name__ == "__main__":
    external_system_demo()
