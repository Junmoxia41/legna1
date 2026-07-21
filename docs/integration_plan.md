# PLAN DE INTEGRACIÓN DE HERRAMIENTAS - LEGNA

Este documento detalla la hoja de ruta para la implementación de los 16 módulos del catálogo de herramientas, asegurando que Legna sea modular, escalable y capaz de interactuar con el mundo exterior.

---

## 1. INFRAESTRUCTURA BASE
Todas las herramientas residen en `legna1/tools/` y siguen el patrón:
- **Categoría**: Una carpeta con un `__init__.py` que registra las herramientas.
- **Herramienta**: Una clase que hereda de `Tool` y define `execute()`.

---

## 2. DETALLE DE INTEGRACIÓN (16 MÓDULOS)

### 1. Sistema de Archivos (`tools/file_tools`)
- **Librerías**: `os`, `shutil`, `pathlib`, `glob`.
- **Herramientas a implementar**: `CreateFile`, `MoveFile`, `DeleteFile`, `SearchTool`, `ArchiveTool` (zip/tar), `FileWatcher` (usando `watchdog`).

### 2. Windows (`tools/windows_tools`)
- **Librerías**: `psutil`, `subprocess`, `winreg`, `wmi`.
- **Herramientas a implementar**: `ProcessManager`, `ServiceControl`, `SystemPower` (Shutdown/Reboot), `HardwareInfo`, `RegistryEditor`.

### 3. CMD / PowerShell (`tools/terminal_tools`)
- **Librerías**: `subprocess`.
- **Herramientas a implementar**: `RunCommand`, `RunPowerShellScript`, `CommandStream` (para obtener salida en tiempo real).

### 4. Python (`tools/python_tools`)
- **Librerías**: `venv`, `pip`, `ast`.
- **Herramientas a implementar**: `ProjectCreator`, `ScriptRunner`, `PackageInstaller`, `CodeAnalyzer`.

### 5. Git y GitHub (`tools/git_tools`)
- **Librerías**: `GitPython`, `PyGithub`.
- **Herramientas a implementar**: `GitClone`, `GitCommit`, `GitPush`, `GitHubIssueManager`, `PRManager`.
- **Seguridad**: Uso de variables de entorno para tokens.

### 6. Navegador (`tools/browser_tools`)
- **Librerías**: `Playwright` o `Selenium`.
- **Herramientas a implementar**: `WebSearch`, `PageNavigator`, `FormFiller`, `WebScraper`.

### 7. Ratón y Teclado (`tools/hid_tools`)
- **Librerías**: `PyAutoGUI`, `pynput`.
- **Herramientas a implementar**: `MouseClick`, `CursorMove`, `KeyboardType`, `ShortcutExecutor`, `ScreenCapture`.

### 8. Visión (`tools/vision_tools`)
- **Librerías**: `OpenCV`, `pytesseract`, `Pillow`.
- **Herramientas a implementar**: `OCRTool`, `ObjectDetector`, `UIRecognizer` (para detectar botones en apps).

### 9. Audio (`tools/audio_tools`)
- **Librerías**: `SpeechRecognition`, `gTTS`, `pyaudio`.
- **Herramientas a implementar**: `VoiceToText`, `TextToSpeech`, `AudioRecorder`, `Player`.

### 10. IA (`tools/ai_tools`)
- **Librerías**: `requests`, adaptadores oficiales (OpenAI, Anthropic).
- **Herramientas a implementar**: `LLMConnector` (Multi-proveedor), `EmbeddingGenerator`, `ImageGenerator`.

### 11. Base de Datos (`tools/db_tools`)
- **Librerías**: `SQLAlchemy`, `sqlite3`, `psycopg2`, `pymongo`.
- **Herramientas a implementar**: `SQLQueryExecutor`, `VectorStoreManager` (Chroma/FAISS), `SchemaExplorer`.

### 12. Memoria (`tools/memory_tools`)
- **Librerías**: Integración interna con `MemoryManager`.
- **Herramientas a implementar**: `MemorySearch`, `ProfileUpdater`, `HabitTracker`, `ContextLoader`.

### 13. Automatización (`tools/automation_tools`)
- **Librerías**: `schedule`, `time`.
- **Herramientas a implementar**: `TaskScheduler`, `WorkflowRunner`, `MacroRecorder`.

### 14. Desarrollo (`tools/dev_tools`)
- **Librerías**: Compiladores del sistema (gcc, dotnet, node).
- **Herramientas a implementar**: `CompilerTool`, `TestRunner`, `DockerManager`.

### 15. Documentos (`tools/doc_tools`)
- **Librerías**: `PyPDF2`, `python-docx`, `openpyxl`, `pandas`.
- **Herramientas a implementar**: `PDFReader`, `ExcelProcessor`, `WordGenerator`, `MarkdownParser`.

### 16. Red (`tools/network_tools`)
- **Librerías**: `requests`, `paramiko` (SSH), `ftplib`.
- **Herramientas a implementar**: `HTTPRequest`, `SSHClient`, `FTPTransfer`, `PortScanner`.

---

## 3. FASES DE IMPLEMENTACIÓN

### Fase A: El Cimiento (Core & OS)
- Implementar **1, 2, 3 y 15**. Esto permite que Legna manipule su propio entorno y documentos.
- *Resultado*: Legna puede leer manuales, crear informes y ejecutar comandos básicos.

### Fase B: Interacción Humana (HID & Multimedia)
- Implementar **7, 8 y 9**.
- *Resultado*: Legna puede "ver" la pantalla, mover el ratón y hablar.

### Fase C: Conectividad & Desarrollo
- Implementar **4, 5, 6, 14 y 16**.
- *Resultado*: Legna puede programar, usar GitHub y navegar por internet.

### Fase D: Inteligencia & Datos
- Implementar **10, 11, 12 y 13**.
- *Resultado*: Legna gestiona bases de datos complejas, usa múltiples IAs y automatiza flujos completos.

---

## 4. INTEGRACIÓN CON EL SISTEMA DE COMANDOS
Cuando el `KnowledgeEngine` detecta una intención:
1. El `CommandManager` identifica la acción.
2. El `CommandManager` solicita la herramienta necesaria al `ToolRegistry`.
3. La `Tool` ejecuta la acción atómica.
4. El resultado vuelve al sistema de memoria como una `Observation`.
