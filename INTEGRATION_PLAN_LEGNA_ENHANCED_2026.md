# PLAN DE INTEGRACIÓN AVANZADA - LEGNA v2.0 (2026)

**Fecha**: 2026-07-21  
**Proyecto base**: legna1 (Junmoxia41)  
**Objetivo**: Transformar Legna en una **compañera neural inteligente** con:
- Gestión avanzada de proyectos y workspace
- Sistema de memoria neuronal tipo cerebro humano
- Editor de código integrado tipo VS Code
- Sistema de saludos ultra-humanos y contextuales
- Importación y análisis de proyectos externos
- Persistencia de conversaciones y recuerdos categorizados

---

## 1. VISIÓN GENERAL

Legna se convertirá en un **entorno completo** que combina:
- Interfaz de escritorio (interfaz heredada + HTML/JS)
- Workspace con gestión de proyectos
- Chat con memoria conversacional
- Editor de código integrado
- Cerebro de memoria con tarjetas neuronales
- Importación inteligente de proyectos externos

Todo se integrará manteniendo la arquitectura modular actual (KnowledgeEngine + MemoryManager + Tools).

---

## 2. NUEVAS FUNCIONALIDADES PRINCIPALES

### 2.1 WORKSPACE - "Crear New Proyecto" + Importar

**Ubicación**: Sección `workspace-section` (ya existe como placeholder)

**Características**:
- **Tarjeta grande principal** (hero card):
  - Fondo con borde cyan
  - Texto grande: **"Crear Nuevo Proyecto"**
  - Subtítulo: "Inicia un nuevo entorno de trabajo"
  - Icono grande + botón "Crear"

- **Botón "Importar Proyecto"**:
  - Abre un diálogo nativo de selección de carpeta (usando `tkinter.filedialog` o interfaz heredada FilePicker)
  - Opciones:
    1. **Mover proyecto** a `/home/user/legna1/workspace/projects/`
    2. **Dejar en ubicación original** + crear symlink / referencia
  - Una vez importado:
    - Escanea recursivamente todos los archivos
    - Genera estructura de árbol
    - Muestra mensaje: "¿Quieres abrir este proyecto con el Editor de Código Legna?"
    - Botones: **Abrir en Editor** | **Ver en Workspace** | **Cancelar**

- **Lista de proyectos**:
  - Tarjetas pequeñas por cada proyecto importado
  - Información: nombre, fecha importación, nº archivos, tamaño

### 2.2 EDITOR DE CÓDIGO INTEGRADO (LegnaCode Editor)

**Tipo**: Clon ligero de VS Code

**Tecnologías**:
- Usar `monaco-editor` (web) dentro de la UI HTML
- O componente interfaz heredada avanzado + CodeMirror si es posible
- O integrar **PyWebView** con Monaco Editor

**Características iniciales**:
- Pestañas de archivos abiertos
- Syntax highlighting (Python, JS, HTML, MD, etc.)
- Barra lateral: Explorador de archivos del proyecto actual
- Panel inferior: Terminal integrada (conexión al sistema de comandos)
- Guardar / Ejecutar / Buscar
- Atajos de teclado básicos (Ctrl+S, Ctrl+F, etc.)

**Integración**:
- Cuando se importa un proyecto → se añade a la lista de proyectos abiertos
- El editor se abre en una nueva sección o modal grande
- Comunicación bidireccional con el backend Python (guardar cambios en disco)

### 2.3 CHAT - Panel Derecho "Conversaciones"

**Cambio dinámico**:
- Actualmente muestra "CORE_ACTIVE"
- Al entrar al chat (`showSection('chat')`):
  - Cambia el panel derecho a:
    - **Título**: "CONVERSACIONES"
    - Lista de conversaciones guardadas (neuronas)
    - Cada una como tarjeta pequeña:
      - Título (primer mensaje o resumen)
      - Fecha/hora
      - Nº de mensajes
      - Botón "Abrir"
    - **Botón grande**: "Nueva Conversación"

**Nueva Conversación**:
- Crea un nuevo thread de chat
- Reinicia el contexto de conversación actual
- Genera saludo nuevo (ver abajo)

### 2.4 SISTEMA DE SALUDOS ULTRA-HUMANOS (50+ variantes)

**Módulo nuevo**: `ai/greeting_engine.py`

**Lógica**:
1. Detectar **fecha/hora** (primero internet → fallback sistema)
2. Detectar **ubicación** (IP geolocalización o sistema)
3. Detectar **si ya saludó hoy** (usando memoria de categoría `saludo_diario`)
4. Elegir saludo contextual + usar nombre del usuario

**Categorías de saludo** (mínimo 50 variantes):

**Mañana (6:00 - 12:00)**:
- "Buenos días [Nombre], ¿cómo amaneciste hoy?"
- "¡Qué bonito verte por aquí tan temprano, [Nombre]!"
- "Hola [Nombre], ¿listo para empezar el día con energía?"
- "Buenos días [Nombre], ¿dormiste bien?"

**Tarde (12:00 - 19:00)**:
- "Buenas tardes [Nombre], ¿cómo va tu día?"
- "¡Hola [Nombre]! ¿Qué tal la tarde?"

**Noche (19:00 - 6:00)**:
- "Buenas noches [Nombre], ¿cómo estuvo tu día?"
- "Hola [Nombre], ¿ya terminaste el día?"

**Variantes especiales**:
- Primera vez del día (usar "amaneciste")
- Basado en clima (si se puede detectar)
- Basado en humor del usuario (análisis simple)
- Variaciones por estación del año
- Saludos creativos / poéticos / divertidos

**Persistencia**:
- Guardar en memoria categoría: `saludo_diario` + fecha

### 2.5 MEMORIA NEURONAL (Brain UI)

**Sección actual**: `memory-section`

**Nueva interfaz**:
- Icono grande de cerebro (SVG animado)
- Al hacer clic → abre modal o sección completa "Cerebro de Legna"

**Dentro del Cerebro**:
- **Grid de tarjetas neuronales** (Memory Cards)
- Cada tarjeta representa un **recuerdo categorizado**
- Estructura de cada recuerdo:
  ```json
  {
    "id": "...",
    "category": "nombre | segundo_nombre | edad | preferencia | comando | hecho | proyecto",
    "key": "nombre",
    "value": "Airien",
    "secondary_value": "Yolexis",
    "confidence": 0.95,
    "timestamp": "...",
    "source": "conversación",
    "notes": "Usuario mencionó su nombre completo"
  }
  ```

**Funcionalidad**:
- **Auto-aprendizaje**:
  - Cada vez que el usuario menciona algo (nombre, edad, comandos, etc.)
  - KnowledgeEngine + nuevos detectores (`CategoryMemoryDetector`)
  - Legna hace preguntas de seguimiento por iniciativa propia:
    - Usuario: "comando ipconfig"
    - Legna: "¿Qué hace el comando ipconfig? ¿Quieres que lo aprenda?"
- **Búsqueda y visualización** por categoría
- **Edición manual** de recuerdos
- **Exportar / Importar** memoria

---

## 3. ARQUITECTURA DE INTEGRACIÓN

### 3.1 Nuevos Módulos

```
/home/user/legna1/
├── workspace/                     # NUEVO
│   ├── projects/                  # Proyectos importados
│   ├── editor/                    # LegnaCode Editor
│   └── project_manager.py
├── ai/
│   ├── greeting_engine.py         # NUEVO
│   ├── conversation_manager.py    # NUEVO
│   └── project_analyzer.py        # NUEVO
├── memory/
│   ├── neural_memory.py           # NUEVO (categorías + tarjetas)
│   └── category_detector.py       # NUEVO
├── ui/
│   ├── workspace_view.py          # NUEVO (interfaz heredada)
│   ├── code_editor.py             # NUEVO (interfaz heredada + Monaco)
│   ├── memory_brain_view.py       # NUEVO
│   └── conversation_panel.py      # NUEVO
├── tools/
│   └── project_tools.py           # NUEVO
```

### 3.2 Flujo de Importar Proyecto

1. Usuario hace clic "Importar Proyecto"
2. Selecciona carpeta
3. `ProjectManager.import_project(path, move=True)`
4. Copia o referencia la carpeta en `workspace/projects/`
5. Escanea archivos → guarda metadatos en DB (`projects` table)
6. Muestra diálogo: "¿Abrir en LegnaCode Editor?"
7. Si acepta → abre editor con el árbol de archivos del proyecto

### 3.3 Flujo de Análisis de Proyecto desde Chat

- Usuario: "analiza el proyecto legna1" o "modifica el archivo main.py"
- `ConversationManager` detecta intención → llama `ProjectAnalyzer`
- Analiza estructura, archivos clave, dependencias
- Propone cambios o abre el editor automáticamente

### 3.4 Sistema de Memoria Neuronal

- Nueva tabla en `database/memory.db`:
  - `neural_memories` (id, category, key, value, metadata, confidence, timestamp)
- Detector especializado: `CategoryMemoryDetector`
- MemoryManager expone:
  - `save_neural_memory(category, key, value, ...)`
  - `get_memories_by_category(category)`
  - `search_neural_memory(query)`

---

## 4. FASES DE IMPLEMENTACIÓN

### Fase 1: Infraestructura (1-2 semanas)
- Crear carpetas `workspace/`, `ai/greeting_engine.py`
- Añadir tablas nuevas a la base de datos
- Implementar `ProjectManager`
- Añadir tarjeta grande "Crear Nuevo Proyecto" en UI

### Fase 2: Importación y Editor Básico (2-3 semanas)
- Implementar importación de proyectos
- Integrar Monaco Editor (o alternativa)
- Crear vista de editor de código
- Diálogo post-importación

### Fase 3: Sistema de Conversaciones y Saludos (1 semana)
- Implementar `GreetingEngine` (50+ saludos)
- Cambiar panel derecho en chat
- Sistema de "Nueva Conversación"
- Persistencia de conversaciones

### Fase 4: Memoria Neuronal (2 semanas)
- `CategoryMemoryDetector`
- UI del Cerebro + tarjetas
- Auto-preguntas de aprendizaje
- Integración con saludo contextual

### Fase 5: Análisis Inteligente y Mejoras (continuo)
- `ProjectAnalyzer`
- Integración completa chat → proyecto
- Mejoras de humanización (contexto de hora/ubicación)

---

## 5. DETALLES TÉCNICOS CLAVE

### Detección de hora e internet
- Usar `requests` + API de hora (worldtimeapi.org)
- Fallback: `datetime` del sistema
- Geolocalización: `ipinfo.io` o similar (opcional)

### Persistencia de conversaciones
- Nueva tabla `conversations`:
  - id, title, created_at, last_message, message_count, context_summary

### Nombre del usuario
- Ya existe en `identity` → usar `nombre` + `segundo_nombre`

### Editor de código
- Recomendación: Integrar **Monaco Editor** vía PyWebView o iframe HTML
- Comunicación: `window.pywebview.api.save_file(path, content)`

---

## 6. PRÓXIMOS PASOS INMEDIATOS

1. **Aprobar este plan** (responder OK)
2. Empezar por **Fase 1**:
   - Crear estructura de carpetas
   - Implementar tarjeta "Crear Nuevo Proyecto"
   - Añadir botón "Importar Proyecto"
3. Crear `greeting_engine.py` con 20 saludos iniciales
4. Actualizar `dashboard.py` y `index.html` para soportar los nuevos paneles

---

**Este documento será la hoja de ruta oficial.**  
¿Quieres que comience la implementación de la Fase 1 ahora?