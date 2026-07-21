from memory.manager import MemoryManager

class LegnaAssistant:
    """
    Clase principal para interactuar con Legna desde otros sistemas.
    Proporciona una interfaz limpia para enviar mensajes y gestionar comandos.
    """
    def __init__(self):
        self.memory_manager = MemoryManager()

    def process_message(self, message):
        """
        Procesa un mensaje, extrae conocimiento, guarda en memoria y ejecuta comandos.
        """
        return self.memory_manager.extract_knowledge(message)

    def add_command(self, command):
        """
        Permite a otros sistemas registrar nuevos comandos dinámicamente.
        """
        self.memory_manager.command_manager.register_command(command)

    def remove_command(self, command_name):
        """
        Permite eliminar comandos.
        """
        self.memory_manager.command_manager.unregister_command(command_name)

    def get_available_commands(self):
        """
        Devuelve la lista de comandos registrados.
        """
        return self.memory_manager.command_manager.list_commands()
