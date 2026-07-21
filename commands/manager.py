import logging

class CommandManager:
    def __init__(self):
        self.commands = {}
        self.logger = logging.getLogger(__name__)

    def register_command(self, command):
        self.commands[command.name] = command
        self.logger.info(f"Comando registrado: {command.name}")

    def unregister_command(self, name):
        if name in self.commands:
            del self.commands[name]
            self.logger.info(f"Comando eliminado: {name}")

    def execute_command(self, trigger, params):
        # Mapeamos el trigger (ej: 'abre') a un comando específico si es necesario
        # Por simplicidad, buscaremos un comando que coincida con el trigger o el nombre
        if trigger in self.commands:
            return self.commands[trigger].execute(params)
        
        # Búsqueda por alias o lógica más compleja podría ir aquí
        for cmd in self.commands.values():
            if hasattr(cmd, 'aliases') and trigger in cmd.aliases:
                return cmd.execute(params)
                
        return f"No se encontró ejecución para el comando: {trigger}"

    def list_commands(self):
        return {name: cmd.description for name, cmd in self.commands.items()}
