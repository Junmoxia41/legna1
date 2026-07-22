# Auditoría integral y plan de refactorización — Legna Workspace IDE

**Fecha:** 2026-07-22  
**Estado:** análisis previo a la migración. No se elimina ningún módulo existente en esta fase.

## 1. Resumen ejecutivo

Legna contiene dos líneas de interfaz que conviven pero no están unificadas:

1. **PyWebView + HTML**: `legna.py` carga `ui/index.html`. Es la interfaz principal y la adecuada para construir un IDE basado en Monaco.

El Workspace actual no es todavía un IDE: los tres editores interfaz heredada duplican responsabilidades y usan `TextField` o WebViews que no disponen de un puente fiable para leer, guardar o sincronizar contenido. El único componente con Monaco real, `ui/monaco_editor.html`, demuestra resaltado sintáctico, pero no gestiona documentos, pestañas ni persistencia de archivos.

**Decisión técnica recomendada:** el nuevo IDE debe ser una aplicación web modular dentro de la ventana PyWebView existente. Monaco se ejecutará una sola vez en `ui/ide/`; Python expondrá una API local explícita, segura y orientada a servicios. 
## 2. Mapa de arquitectura actual

### Puntos de entrada y ventanas

| Componente | Tecnología | Responsabilidad actual | Estado |
|---|---|---|---|
| `legna.py` | PyWebView | Shell principal, API de proyectos, memoria, chat y agentes | Activo, destino del IDE |
| `ui/index.html` | HTML/JS | Dashboard, chat, workspace simple, memoria, agentes y perfil | Activo |
| `ui/monaco_webview.py` | PyWebView | Ventana Monaco aislada | Prototipo; no carga/guarda archivo |
| `ui/real_terminal_window.py` | PyWebView | Ventana de terminal aislada | Incompleto: API no expuesta |
| `ui/monaco_editor.html` | HTML/Monaco | Instancia básica de Monaco desde CDN | Reutilizable como referencia, no como shell final |

### Workspace y editor

| Módulo | Capacidades existentes | Limitación principal |
|---|---|---|
| `workspace/project_manager.py` | crear, importar, listar, eliminar metadatos y escanear archivos | rutas/validación insuficientes, no hay workspaces múltiples ni estado IDE |
| `ui/code_editor.py` | árbol plano, tabs básicas, leer/escribir con `TextField` | editor simple; no terminal/Monaco real |
| `ui/enhanced_code_editor.py` | tabs, modificaciones, terminal e intento de Monaco | mezcla UI, estado, IO y terminal; referencias no válidas a `MonacoWebView` |
| `ui/legna_monaco_editor.py` | toolbar, árbol, terminal y WebView | no pasa contenido al Monaco ni recupera cambios; ruta absoluta Linux; no hay tabs reales |
| `ui/monaco_editor.html` | idiomas, minimapa y opciones básicas | carga contenido por `postMessage`, pero nadie implementa el puente completo |
| `ui/real_terminal.py` | ejecuta un comando de shell en hilo | shell libre, un único terminal, sin sesiones ni política de seguridad |

### Servicios, IA y memoria

| Área | Módulos reutilizables |
|---|---|
| Chat e identidad | `services/chat_service.py`, `ai/context_engine.py`, `ai/personality_engine.py` |
| Orquestación de agentes | `brain/orchestrator.py`, `brain/scheduler.py`, `agents/registry.py` |
| Modelos locales | `models/manager.py`, `models/scanner.py`, `models/runtime.py`, `models/router.py`, `models/reliability.py` |
| Memoria | `memory/neural_memory.py`, `memory/conversation_manager.py`, SQLite legado en `memory/database.py` |
| Herramientas | `tools/registry.py` y categorías de archivo, Python, Git, red y sistema |

La integración de IA actual ya es suficiente como base para un `AIWorkspaceService`: Legna Brain identifica código, Core coordina agentes y Code/Quality pueden especializar el prompt. Aún no existe integración con un documento de editor, una selección o un diff aplicado.

## 3. Comunicación actual y problemas de integración

### Comunicación actual

```text
HTML actual → window.pywebview.api → LegnaAPI → servicios Python
Monaco HTML → postMessage parcial → sin receptor fiable ni API de archivos
```

### Problemas críticos detectados

1. Hay tres implementaciones de editor (`LegnaCodeEditor`, `EnhancedLegnaCodeEditor`, `LegnaMonacoEditor`) con comportamiento superpuesto.
2. Monaco no recibe el contenido real del archivo desde el editor interfaz heredada y el método de guardar es un placeholder.
3. `LegnaMonacoEditor` usa la ruta absoluta `/home/user/legna1/...`; falla fuera de ese entorno.
4. El árbol de archivos es plano, limitado artificialmente y no permite navegación por directorios real.
5. `ProjectManager.scan_project_files()` recorre todo sin exclusiones, caché, límites por tamaño ni lazy loading.
6. Terminal y herramientas Git usan `shell=True` o comandos libres; no deben exponerse al asistente o a la UI sin una política de autorización.
7. Las operaciones de archivo existentes aceptan rutas arbitrarias, sin un sandbox de workspace ni defensas contra path traversal.
8. No existe capa de estado: pestañas, selección, paneles, cursor, layout y sesiones se viven dentro de clases UI.
9. No hay servicio de Git estructurado: `git_ops.py` solo contiene clone/commit/push y no entrega estado, diff, ramas, conflictos ni staging.
10. No hay indexador, búsqueda global, diagnósticos, plugins ni API de eventos.

## 4. Principio de compatibilidad

No se eliminarán los módulos actuales durante la migración. Se aplicará el patrón **adaptador + sustitución progresiva**:

- `ProjectManager` seguirá siendo la fuente de proyectos registrados, evolucionado por un servicio compatible.
- - `ui/monaco_editor.html` se conserva como prototipo/referencia; el nuevo IDE tendrá su propia app modular.
- `RealTerminal` no se reutilizará directamente para comandos del IDE; su comportamiento se encapsulará tras una política de terminal.
- Agentes, memoria y chat se consumen por interfaces de servicio sin acoplarse a componentes HTML.

## 5. Arquitectura objetivo

```text
PyWebView shell (legna.py)
      │
      ├── ui/ide/index.html                 ← UI modular de IDE
      │      ├── state/                      ← estado, eventos, layout, atajos
      │      ├── components/                 ← explorer, tabs, editor, panel inferior
      │      ├── panels/                     ← terminal, problemas, git, IA
      │      └── monaco/                     ← bridge, modelos, comandos
      │
      └── ide/                               ← backend Python
             ├── api.py                      ← fachada PyWebView versionada
             ├── workspace_service.py        ← raíces, proyectos, recientes, favoritos
             ├── filesystem_service.py       ← operaciones seguras y árbol lazy
             ├── document_service.py         ← lectura/escritura, hashes, externos
             ├── session_service.py          ← tabs, cursor, layout, terminales
             ├── search_service.py           ← archivo/texto/símbolo, indexación
             ├── terminal_service.py         ← sesiones, proceso, salida, permisos
             ├── git_service.py              ← status, diff, branch, commit, pull/push
             ├── diagnostics_service.py      ← problemas y analizadores
             ├── ai_workspace_service.py     ← Legna Core/Code sobre contexto de editor
             ├── plugins/                    ← contrato y registro de plugins
             ├── events.py                   ← eventos tipados
             └── policy.py                   ← autorización y sandbox
```

### Reglas de diseño

- El frontend no accede al sistema de archivos directamente; solo usa la API del IDE.
- Cada operación recibe un `workspace_id` y se valida contra sus raíces autorizadas.
- El contenido no se inserta con `innerHTML` sin escaping; se usan nodos DOM seguros.
- Terminal, Git push/pull, borrado, movimiento y aplicación de cambios IA requieren permiso explícito.
- Monaco es el editor de texto; el backend solo persiste documentos y proporciona servicios.
- El frontend mantiene el estado de interacción; `SessionService` persiste el estado recuperable.

## 6. Componentes del IDE y nivel de implementación

| Componente solicitado | Estado actual | Estrategia de migración |
|---|---|---|
| Explorador jerárquico | No existe | `FilesystemService` + `ExplorerController`, carga por carpeta |
| Crear/renombrar/mover/borrar | Parcial/no seguro | operaciones validadas + confirmación + papelera |
| Drag & drop | Placeholder interfaz heredada | drag/drop HTML, backend `move` validado |
| Tabs / splits | Muy parcial | `TabsState`, modelos Monaco por documento, layouts de grupos |
| Monaco | Parcial | una instancia administrada por `EditorManager`, bridge completo |
| Terminal múltiple | Una terminal libre | sesiones con stream, cwd, historial, cancelación y policy |
| Git | Herramientas aisladas | `GitService` basado en subprocess sin shell, panel de estado/diff |
| IA contextual | Chat separado | `AIWorkspaceService` con selección/documento/diff, no acceso implícito |
| Memoria IDE | No existe | `SessionService` y memoria de proyecto con consentimiento |
| Búsqueda global | Placeholder | índice incremental y búsqueda paginada |
| Problemas | No existe | formato diagnóstico unificado, Python primero |
| Plugins | No existe | manifiesto, hooks y registro de comandos/paneles |
| Atajos | No existe | `ShortcutManager` frontend con command registry |
| Temas/accesibilidad | Tema oscuro fijo | tokens CSS, dark/light, zoom y preferencias |

## 7. Fases de ejecución

### Fase 0 — Fundamentos y seguridad

1. Crear paquete `ide/` y servicio API sin cambiar pantallas existentes.
2. Implementar `WorkspaceService`, `FilesystemService`, `DocumentService` y `SessionService`.
3. Definir modelos de datos y eventos; añadir pruebas temporales.
4. Establecer sandbox por workspace, validación de rutas, exclusiones (`.git`, `node_modules`, `.venv`, binarios) y límites de tamaño.

**Resultado:** API segura para proyectos, árbol lazy, documentos y estado; sin nueva UI aún.

### Fase 1 — Shell IDE + Monaco real

1. Crear `ui/ide/index.html` y módulos JS/estilos propios de Legna.
2. Toolbar, activity bar, Explorer jerárquico, tabs, área Monaco, status bar y panel inferior colapsable.
3. Bridge Monaco: abrir, editar, dirty state, guardar, autosave, cursor, lenguaje, comandos y atajos principales.
4. Persistir tabs/layout/cursor y restaurarlos al reiniciar.

**Resultado:** IDE de un proyecto usable sin perder datos, reemplazando solo el botón “Abrir” del Workspace PyWebView.

### Fase 2 — Productividad local

1. Crear/renombrar/copiar/cortar/pegar/duplicar/mover/eliminar con menú contextual y confirmaciones.
2. Búsqueda por archivo/texto, filtros, favoritos, recientes y workspaces múltiples.
3. Problemas: diagnósticos Python mediante compilación/linter opcional y navegación a línea.
4. Terminales múltiples con procesos controlados, historial, cancelación y perfiles Windows/POSIX.

### Fase 3 — Git y paneles

1. Estado, staged/unstaged, diff, ramas, commits y conflictos.
2. Pull/push/stash bajo confirmación y credenciales gestionadas localmente, nunca por chat.
3. Salida, Git, terminal y problemas como paneles intercambiables.

### Fase 4 — IA de editor y agentes

1. Panel contextual Legna: explicar, documentar, pruebas, refactor, optimizar y corregir.
2. Legna Brain enruta automáticamente a Code/Quality/Research según documento y selección.
3. Toda modificación IA se presenta como preview/diff; el usuario acepta o rechaza.
4. Memoria de proyecto con controles visibles y feedback de calidad.

### Fase 5 — Extensibilidad y rendimiento

1. Plugin API con manifiestos, comandos, paneles, menús y atajos.
2. Indexador incremental, cachés, workers y virtualización en listas extensas.
3. Temas, modo claro, escala de interfaz, fuentes y accesibilidad de teclado.

## 8. Prioridades y exclusiones iniciales

La promesa de “IDE profesional” se debe construir por capas, no imitando visualmente a otros editores. Las primeras entregas deben priorizar integridad de archivos, guardado real, sesiones, Monaco y permisos.

No se habilitarán inicialmente:

- ejecución libre de terminal desde prompts IA;
- push a GitHub mediante tokens compartidos;
- borrado irreversible;
- carga de proyectos enteros en memoria;
- aplicación automática de cambios generados por IA.

## 9. Criterios de aceptación para la primera entrega IDE

- Abrir uno o más proyectos registrados.
- Árbol real lazy y seguro, con carpetas expandibles.
- Abrir varios archivos en tabs Monaco.
- Marcar documentos modificados, guardar con Ctrl+S y restaurar sesión.
- Resaltado para lenguajes solicitados por Monaco.
- Búsqueda de archivos y texto inicial.
- Sin rutas absolutas de `/home/user` en la nueva implementación.
- Sin `shell=True` dentro de los servicios nuevos.
- Pruebas para sandbox de rutas, documentos, sesiones y operaciones de archivos.
