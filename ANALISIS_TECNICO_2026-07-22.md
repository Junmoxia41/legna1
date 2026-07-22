# Análisis técnico del repositorio Legna

**Fecha:** 2026-07-22  
**Alcance:** revisión estática del repositorio, compilación Python, prueba de importación y ejecución de la suite pytest existente. No se utilizó ninguna credencial.

## 1. Resumen ejecutivo

Legna es un prototipo Python de asistente personal con cuatro líneas de trabajo parcialmente superpuestas:

1. **Núcleo legado de conocimiento y comandos**: `assistant.py`, `memory/`, `commands/` y `tools/`.
2. **Memoria neuronal y conversaciones JSON**: `memory/neural_memory.py` y `memory/conversation_manager.py`.
3. **Workspace de proyectos**: `workspace/project_manager.py`.
4. **Dos interfaces distintas**: interfaz heredada (`ui/main_app.py`) y PyWebView/HTML (`legna.py`, `ui/index.html`).

La base modular es aprovechable y el código compila, pero las integraciones que convierten los módulos en una aplicación completa no están terminadas. La prioridad debe ser definir un único flujo de ejecución y conectar el chat real con LLM, memoria, conversación y herramientas de forma segura.

## 2. Estructura y flujos actuales

### Núcleo de conocimiento

`LegnaAssistant.process_message()` delega en `MemoryManager.extract_knowledge()`.

Flujo actual:

```text
mensaje -> KnowledgeEngine -> detectores -> MemoryEvaluation[]
        -> ShortTermMemory -> SQLite observations
        -> CommandManager (solo para evaluaciones command)
```

Los detectores identifican preferencias, hechos, objetivos, hábitos, contradicciones, repeticiones y comandos. `ShortTermMemory` convierte evaluaciones guardables en observaciones SQLite.

### Memoria y conversación de la interfaz moderna

Existe una segunda vía, independiente del flujo anterior:

- `NeuralMemoryManager`: persiste recuerdos por categorías en JSON.
- `ConversationManager`: persiste conversaciones en JSON.
- `ContextEngine`: construye contexto a partir de la memoria neuronal.

Estas clases no se conectan con `MemoryManager` ni con el chat PyWebView actual.

### Interfaces

- `ui/main_app.py`: aplicación interfaz heredada, con pantallas de chat, dashboard, editor, memoria y workspace.
- `legna.py`: aplicación PyWebView que carga `ui/index.html` y expone una API a JavaScript.
- `ui/monaco_webview.py` y `ui/real_terminal_window.py`: abren más ventanas PyWebView.

No hay un punto de entrada único, ni una estrategia de navegación/integración común entre interfaz heredada y PyWebView.

## 3. Validaciones realizadas

| Comprobación | Resultado |
|---|---|
| Compilación `python -m compileall` | Correcta |
| `pytest -q` | 3 pruebas pasan |
| Importación de módulos de núcleo | Correcta |
| Importación de `legna` | Falla en este entorno: falta el paquete `webview`/`pywebview` instalado |
| Suite `unittest discover` | No descubre pruebas (las pruebas son de estilo pytest) |

Las tres pruebas pytest son demostraciones con `print` y prácticamente no contienen aserciones. Por tanto, confirman que no se produjo una excepción, pero no validan resultados, errores ni seguridad. Además realizan operaciones de escritura y ejecución local.

## 4. Hallazgos prioritarios

### P0 — Chat PyWebView no es funcional como asistente

En `legna.py`, `LegnaAPI.process_chat()` solo devuelve un eco del mensaje:

```python
return f"Entendido. He procesado tu mensaje: {message}"
```

No llama a `LLMClient`, `ContextEngine`, `ConversationManager`, `NeuralMemoryManager`, `MemoryManager`, `ModelRouter` ni `PersonalityEngine`. Las capacidades anunciadas no llegan al usuario de esa interfaz.

**Acción:** crear un servicio de chat único que valide el mensaje, cargue/cree conversación, genere contexto, consulte al proveedor LLM, persista mensaje y respuesta, y devuelva una respuesta estructurada.

### P0 — Dos arquitecturas de UI sin integración

interfaz heredada y PyWebView son aplicaciones distintas. También se intentan abrir ventanas PyWebView anidadas desde funcionalidades de interfaz heredada. Esto causa puntos de arranque confusos y una experiencia inconsistente.

**Acción:** elegir una UI principal (recomendación: mantener PyWebView+HTML si el objetivo es Monaco web, o interfaz heredada si se prioriza Python nativo) y convertir la otra en código retirado o migrado. Definir un único comando de arranque.

### P0 — Herramientas potentes sin autorización, aislamiento ni límites

El registro incorpora archivos, terminal/sistema, Python, Git, GitHub, red, navegador, automatización, base de datos, teclado, ratón y visión. Algunas herramientas ejecutan comandos o scripts y trabajan con rutas libres. No hay una capa común de:

- confirmación explícita antes de acciones destructivas o externas;
- lista permitida de directorios de trabajo;
- política de red o destinos permitidos;
- límites de tiempo, salida y tamaño;
- auditoría de quién solicitó cada operación.

**Acción:** antes de conectar herramientas al chat, implementar un `ToolExecutionPolicy` central con permisos por riesgo, workspace restringido, confirmación humana y registros de auditoría. No exponer ejecución de comandos directamente a texto no confiable.

### P1 — Memoria fragmentada y aprendizaje incompleto

Hay tres almacenamientos: SQLite (`memory.db`), JSON de memoria neuronal y JSON de conversaciones. El diseño de consolidación no está implementado. En particular:

- `Database.clear_expired_observations()` contiene `pass`.
- `History` contiene solo placeholders.
- No existen `Statistics` ni `MemoryConsolidator`.
- Las observaciones nunca se consolidan en memoria permanente mediante el flujo del núcleo.
- El editor visual de memoria muestra éxito, pero `_save_new_memory()` no persiste nada; editar memoria también es TODO.

**Acción:** definir una fuente de verdad y un esquema común. Inicialmente, conviene conservar SQLite como persistencia principal, añadir conversaciones allí o mediante un repositorio claro, e implementar expiración + consolidación con pruebas.

### P1 — Gestión de proyectos frágil

`ProjectManager` usa una ruta absoluta específica: `/home/user/legna1/workspace`. Esto impide que funcione correctamente en otro equipo. También permite nombres de proyecto no saneados, duplica metadatos al crear el mismo proyecto y usa `except:` genéricos.

**Acción:** configurar la raíz con `Path(__file__)`, variable de entorno o archivo de configuración; validar nombres; evitar duplicados; usar UUID; manejar excepciones específicas; excluir directorios pesados al escanear.

### P1 — Configuración de LLM y router no conectados

`LLMClient` usa una URL y un modelo fijos en `config.py`. `ModelRouter` solo retorna diccionarios; no selecciona realmente un modelo ni se usa en el cliente. Faltan configuración por entorno, comprobación de disponibilidad, reintentos controlados, historial de mensajes y errores estructurados.

**Acción:** usar configuración tipada desde variables de entorno o `.env` no versionado; unificar el cliente y router; incorporar contexto y conversación; establecer timeout y manejo de errores sin filtrar detalles internos al usuario.

### P1 — Documentación contradictoria

El README declara versión 0.3 y dice `python main.py`; `main.py` es una demo del núcleo, no la interfaz. Otros documentos afirman que el proyecto está listo para producción, pero indican scripts inexistentes: `run_legna_final.py` y `run_legna_v2_final.py`.

**Acción:** crear un README honesto y único con instalación, dependencias, comando de ejecución, limitaciones y arquitectura vigente; retirar o marcar como histórico los documentos obsoletos.

## 5. Hallazgos secundarios

- `requirements.txt` es amplio y no está fijado por versiones; no hay lockfile ni instrucciones de instalación por plataforma.
- Faltan pruebas unitarias reales para detectores, base de datos, conversación, memoria, workspace, API del chat y políticas de herramientas.
- Las pruebas actuales escriben en archivos/datos del repositorio y ejecutan procesos; deben usar `tmp_path`, mocks y aserciones.
- Hay `except:` amplios que ocultan corrupción de datos o fallos de IO.
- La base abstracta `Command.execute()` y `Tool.execute()` contienen `pass`; deberían ser métodos abstractos efectivos o lanzar `NotImplementedError` si se instancian clases base.
- `GreetingEngine` consulta un servicio externo de hora; debe tener fallback local fiable y no bloquear el inicio por una llamada de red.
- `DeepProjectAnalyzer` y módulos de personalidad/router aportan lógica aislada, pero no están integrados en el flujo de usuario.
- Hay archivos de base de datos versionados. Debe definirse si son datos de muestra; en producción los datos de usuario no deberían entrar al repositorio.

## 6. Hoja de ruta recomendada

### Fase A — Estabilizar la base

1. Elegir UI y crear un único punto de entrada documentado.
2. Normalizar configuración y dependencias.
3. Corregir las rutas absolutas y los errores silenciados.
4. Separar demos de las pruebas automatizadas; añadir pruebas con aserciones y almacenamiento temporal.
5. Actualizar README y eliminar referencias a scripts inexistentes.

### Fase B — Chat útil y persistente

1. Crear `ChatService` como único orquestador.
2. Conectar LLM local, contexto, conversación y memoria.
3. Añadir identificador de conversación a la API y persistir ambos roles.
4. Exponer respuestas y errores en un formato consistente.
5. Integrar saludo, personalidad y análisis de intención desde ese servicio.

### Fase C — Memoria confiable

1. Decidir un repositorio principal y migrar los datos existentes si corresponde.
2. Implementar expiración de observaciones.
3. Diseñar e implementar estadísticas y consolidación.
4. Implementar alta, edición y borrado real en la vista de memoria.
5. Añadir recuperación contextual con límites y privacidad.

### Fase D — Herramientas seguras

1. Añadir política central de autorización y auditoría.
2. Restringir archivos al workspace y evitar traversal de rutas.
3. Requerir confirmación para red, procesos, Git/GitHub y cambios destructivos.
4. Introducir timeouts, validación de argumentos y resultados tipados.
5. Solo entonces permitir que el modelo solicite herramientas.

## 7. Primera función recomendada para implementar

La función con mayor valor inmediato es **un chat real y persistente**: sustituir el eco de `process_chat` por un servicio que use LM Studio, guarde mensajes en una conversación, añada contexto de memoria y se integre con una única interfaz. Debe hacerse junto con pruebas y validación de errores, pero sin habilitar ejecución automática de herramientas todavía.
