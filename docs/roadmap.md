# ROADMAP
## Proyecto Jarvis

Versión: 0.3

---

# Estado del Proyecto

Proyecto:

Jarvis

Asistente:

Legna

Estado:

En desarrollo.

Objetivo principal:

Construir una compañera digital capaz de comprender el contexto del usuario, aprender con el tiempo y ayudar de forma proactiva.

---

# FASE 1 - Fundación

## Arquitectura

- [x] Crear estructura inicial del proyecto.
- [x] Configurar Visual Studio Code.
- [x] Integrar LM Studio.
- [x] Crear LLMClient.
- [x] Comunicación con el modelo de lenguaje.
- [x] Manejo básico de errores.

## Memoria

- [x] Crear MemoryManager.
- [x] Crear módulo Database.
- [x] Inicialización automática de la carpeta database.
- [x] Creación automática de memory.db.
- [x] Creación automática de tablas.
- [x] Sistema de metadata.
- [x] Versionado del esquema (schema_version).

---

# FASE 2 - Motor de Conocimiento

## Arquitectura

- [x] Diseñar la arquitectura general del sistema de conocimiento.
- [x] Crear modelo Memory.
- [x] Crear modelo MemoryEvaluation.
- [x] Crear DetectorRegistry.
- [x] Crear KnowledgeEngine.
- [x] Separar lógica y conocimiento mediante language.py.
- [x] Crear TextExtractor.
- [x] Adaptar MemoryManager al nuevo flujo.

---

## Detectores

### Implementados

- [x] PreferenceDetector.
- [x] FactDetector.

### Pendientes

- [ ] GoalDetector.
- [ ] HabitDetector.
- [ ] TaskDetector.
- [ ] EventDetector.
- [ ] RelationshipDetector.
- [ ] ContradictionDetector.
- [ ] EmotionDetector.

---

## Evaluación

Implementado:

- [x] Sistema de importancia.
- [x] Sistema de confianza.
- [x] Polaridad.
- [x] Persistencia.
- [x] Detección múltiple por mensaje.
- [x] Extracción modular mediante TextExtractor.

Pendiente:

- [ ] Sistema de pesos por trigger.
- [ ] Detección contextual.
- [ ] Ajuste automático de confianza.
- [ ] Normalización avanzada del lenguaje.

---

# FASE 3 - Sistema de Memoria

## Modelos

- [x] Memory.
- [x] MemoryEvaluation.
- [ ] Observation.

---

## Memoria a corto plazo

- [ ] ShortTermMemory.
- [ ] Tabla observations.
- [ ] Registro automático de observaciones.
- [ ] Eliminación automática de observaciones expiradas.

---

## Consolidación

- [ ] Statistics.
- [ ] MemoryConsolidator.
- [ ] Conversión Observation → Memory.
- [ ] Consolidación automática de recuerdos.

---

## Memoria permanente

Implementado:

- [x] Guardado manual.
- [x] Carga de recuerdos.

Pendiente:

- [ ] Actualización de recuerdos.
- [ ] Recuperación inteligente.
- [ ] Búsqueda semántica.
- [ ] Refuerzo por repetición.
- [ ] Degradación temporal.

---

## Historial

- [ ] Registro de eventos de memoria.
- [ ] Auditoría de cambios.
- [ ] Seguimiento de consolidaciones.

---

## Papelera

- [ ] Eliminación lógica.
- [ ] Restauración de recuerdos.
- [ ] Eliminación definitiva tras periodo de seguridad.

---

# FASE 4 - Comprensión

- [x] JSON estructurado.
- [x] Interpretación de intenciones.
- [x] Sistema de comandos (Implementado v0.4).
- [x] Clasificación automática de solicitudes.
- [ ] Primeras acciones sobre Windows.

---

# FASE 5 - Automatización

- [ ] Apertura de aplicaciones.
- [ ] Control de archivos.
- [ ] Control básico del sistema.
- [ ] Automatización de tareas.

---

# FASE 6 - Identidad

- [ ] Crear Identity.
- [ ] Definir personalidad.
- [ ] Definir principios.
- [ ] Definir estilo de comunicación.
- [ ] Integrar Identity.

---

# FASE 7 - Aprendizaje

- [ ] Aprendizaje estadístico.
- [ ] Aprendizaje de hábitos.
- [ ] Aprendizaje de preferencias.
- [ ] Aprendizaje de relaciones.
- [ ] Organización inteligente de recuerdos.
- [ ] Olvido inteligente.

---

# FASE 8 - Planificación

- [ ] Gestión de objetivos.
- [ ] Seguimiento de proyectos.
- [ ] Organización de tareas.
- [ ] Priorización.

---

# FASE 9 - Proactividad

- [ ] Detección de contexto.
- [ ] Recomendaciones.
- [ ] Recordatorios inteligentes.
- [ ] Intervención cuando aporte valor.

---

# FASE 10 - Integración

- [ ] Calendario.
- [ ] Correo.
- [ ] Navegador.
- [ ] Archivos.
- [ ] Aplicaciones externas.

---

# FASE 11 - Voz

- [ ] Activación por voz.
- [ ] Conversación continua.
- [ ] Síntesis de voz.
- [ ] Reconocimiento de hablantes.

---

# FASE 12 - Compañera Digital

Objetivo final.

Legna deberá ser capaz de:

- comprender el contexto;
- mantener memoria a largo plazo;
- aprender de la experiencia;
- consolidar recuerdos automáticamente;
- organizar su conocimiento;
- ayudar a alcanzar objetivos;
- actuar de forma proactiva;
- mantener una identidad propia;
- funcionar incluso sin conexión a Internet;
- utilizar distintos modelos de lenguaje sin depender de uno en particular.

---

# Ideas en estudio

Estas ideas forman parte de la visión del proyecto, pero todavía no se implementarán.

- Bases de datos especializadas por responsabilidad.
- Sistema avanzado de detectores.
- Motor estadístico de aprendizaje.
- Sistema de seguridad contextual.
- Gestión avanzada de objetivos.
- Aprendizaje continuo.
- Sistema de iniciativa.
- Sustituir LM Studio por un motor integrado.
- Ejecutable independiente.