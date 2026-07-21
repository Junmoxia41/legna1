from tools.base import ToolCategory

class VisionToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="VisionTools", description="Herramientas de visión artificial y OCR")

class MouseToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="MouseTools", description="Control del cursor y clics")

class KeyboardToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="KeyboardTools", description="Simulación de teclado y atajos")

class PythonToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="PythonTools", description="Gestión de proyectos y ejecución de scripts Python")

class GitToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="GitTools", description="Operaciones de Git local")

class GithubToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="GithubTools", description="Integración con la API de GitHub")

class BrowserToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="BrowserTools", description="Automatización de navegación web")

class AudioToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="AudioTools", description="Reconocimiento y síntesis de voz")

class NetworkToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="NetworkTools", description="Protocolos de red y APIs")

class DatabaseToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="DatabaseTools", description="Gestión de bases de datos SQL y NoSQL")

class AutomationToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="AutomationTools", description="Flujos de trabajo y macros")

class DeveloperToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="DeveloperTools", description="Herramientas para múltiples lenguajes de desarrollo")

class MemoryToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="MemoryTools", description="Acceso directo a sistemas de memoria")

class AIProviderToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="AIProviderTools", description="Adaptadores para diferentes proveedores de IA")

class UtilityToolsCategory(ToolCategory):
    def __init__(self):
        super().__init__(name="UtilityTools", description="Utilidades generales")
