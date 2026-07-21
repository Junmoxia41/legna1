# RULEBOOK
## Proyecto Jarvis

Versión: 0.3

---

# Propósito

Este documento define las reglas permanentes de desarrollo del proyecto.

No describe la arquitectura.

No describe el roadmap.

Su objetivo es establecer los principios que deberán respetarse durante toda la evolución de Legna.

---

# Proyecto

Nombre del proyecto:

Jarvis

Nombre del asistente:

Legna

---

# Filosofía del proyecto

Legna no es un chatbot.

Legna es una compañera digital cuyo propósito es comprender el contexto del usuario, ayudarle a alcanzar sus objetivos y actuar de forma proactiva cuando pueda aportar un beneficio real.

Los modelos de lenguaje son únicamente motores de razonamiento.

Nunca representan la inteligencia de Legna.

La inteligencia deberá surgir de la cooperación entre:

- memoria;
- aprendizaje;
- identidad;
- planificación;
- contexto;
- automatización;
- criterio propio.

---

# Filosofía de desarrollo

Siempre se seguirá el siguiente orden:

Arquitectura

↓

Implementación

↓

Pruebas

↓

Optimización

Nunca al contrario.

---

## Desarrollo incremental

El proyecto siempre avanzará paso a paso.

Cada etapa deberá estar completamente probada antes de comenzar la siguiente.

No se implementarán sistemas complejos antes de necesitarlos.

La infraestructura únicamente se desarrollará cuando exista una necesidad real dentro de la arquitectura.

---

## Calidad

Siempre se priorizará:

Primero correcto.

Después rápido.

La claridad del código tendrá prioridad sobre escribir menos líneas.

---

# Principios de diseño

- Cada módulo tendrá una única responsabilidad.
- Los módulos deberán estar desacoplados siempre que sea posible.
- Todo componente deberá poder sustituirse sin romper el resto del sistema.
- La arquitectura tendrá prioridad sobre las nuevas funcionalidades.
- El conocimiento deberá estar separado de la lógica.
- La implementación deberá reflejar el diseño definido en architecture.md.
- Los módulos de coordinación no deberán contener lógica de negocio.
- Los sistemas deberán comunicarse mediante modelos del dominio siempre que sea posible.

---

# Principios de memoria

La memoria permanente será independiente del modelo de lenguaje.

El aprendizaje deberá continuar funcionando incluso sin conexión a Internet.

Los modelos de lenguaje podrán actuar como asesores.

Nunca como una dependencia obligatoria.

El sistema de memoria estará dividido en etapas claramente diferenciadas:

- Observación.
- Memoria a corto plazo.
- Consolidación.
- Memoria a largo plazo.

Cada etapa deberá mantener una única responsabilidad.

---

# Aprendizaje

Legna dispondrá de dos mecanismos de aprendizaje.

## Aprendizaje implícito

Legna evaluará automáticamente la información recibida mediante el KnowledgeEngine y sus detectores especializados.

Las evaluaciones generadas podrán convertirse posteriormente en observaciones y, tras el proceso de consolidación, en recuerdos permanentes.

## Aprendizaje explícito

El usuario podrá ordenar directamente almacenar información.

Ejemplos:

- "Recuerda que..."
- "Guarda que..."
- "Añade a tus preferencias..."

Ambos mecanismos deberán convivir dentro de la misma arquitectura.

---

# Modelos del dominio

Siempre que aparezca un concepto importante dentro de Legna deberá estudiarse si merece convertirse en un modelo propio.

Modelos actuales:

- Memory
- MemoryEvaluation
- Observation

Modelos futuros:

- Goal
- Task
- Identity
- Habit
- Event

Los modelos representan conceptos propios de Legna.

No contienen lógica de negocio.

---

# Base de datos

Durante las primeras fases existirá una única base de datos.

memory.db

Contendrá progresivamente tablas como:

- memories
- observations
- conversations
- metadata

En el futuro podrán añadirse:

- history
- trash

La arquitectura deberá permitir dividir esta base en varias bases especializadas sin modificar el funcionamiento del resto del proyecto.

Database será el único responsable de la persistencia.

---

# Sistema de conocimiento

El sistema encargado de comprender el lenguaje estará completamente separado del sistema de memoria.

Los detectores tendrán una única responsabilidad.

Todos producirán objetos MemoryEvaluation.

Los detectores nunca almacenarán recuerdos.

Nunca conocerán SQLite.

Nunca dependerán unos de otros.

---

# Sistema de comandos

El sistema de comandos debe ser extensible y escalable.

Cada comando debe ser una clase independiente que herede de una clase base común.

El CommandManager será el encargado de registrar, eliminar y ejecutar los comandos.

El sistema de memoria actuará como filtro previo, identificando cuándo un mensaje contiene una orden y delegando su ejecución al sistema de comandos.

Legna debe poder recibir órdenes de otros sistemas a través de una interfaz limpia (Assistant Facade), sin depender exclusivamente de un input de usuario directo.

---

# Proactividad

Legna no deberá limitarse a responder preguntas.

Su objetivo será comprender el contexto del usuario y ayudar cuando pueda aportar un beneficio real.

La proactividad siempre deberá estar basada en:

- contexto;
- memoria;
- objetivos;
- evidencia.

Nunca en suposiciones.

---

# Privacidad

La privacidad será un principio fundamental.

En futuras versiones existirá un sistema de seguridad contextual encargado de decidir cuándo una acción requiere confirmación.

---

# Reglas de programación

- Cada archivo deberá tener una única responsabilidad.
- Los archivos pequeños son preferibles a los archivos grandes.
- Si una clase empieza a asumir varias responsabilidades deberá dividirse.
- Siempre que sea posible se utilizarán modelos del dominio en lugar de largas listas de parámetros.
- Siempre que exista una solución basada en niveles (importancia, confianza, prioridad, riesgo...) se preferirá frente a decisiones binarias cuando aporte claridad al diseño.
- Primero se diseña la arquitectura. Después se implementa el código.
- Todo módulo nuevo deberá diseñarse pensando en su crecimiento futuro sin implementar funcionalidades innecesarias.
- Los componentes deberán ser reutilizables siempre que sea posible.
- Las utilidades generales deberán permanecer independientes de la lógica de negocio.

---

# Flujo de desarrollo

Antes de comenzar una nueva funcionalidad deberán definirse:

- su responsabilidad;
- sus dependencias;
- cómo interactúa con el resto del sistema;
- cómo podrá evolucionar en el futuro.

Solo después comenzará la implementación.

Cada paso deberá probarse antes de continuar con el siguiente.

---

# Gestión de la documentación

Los tres documentos oficiales del proyecto son:

- rulebook.md
- architecture.md
- roadmap.md

Siempre que se tome una decisión importante de arquitectura o antes de continuar el proyecto en un nuevo chat, los tres documentos deberán revisarse y actualizarse conjuntamente.

Ningún documento deberá quedar desincronizado con los demás.

---

# Objetivo final

Construir una compañera digital capaz de:

- comprender el contexto del usuario;
- mantener memoria a largo plazo;
- aprender de forma autónoma;
- organizar sus propios recuerdos;
- ayudar a alcanzar objetivos;
- actuar de forma proactiva;
- mantener una identidad propia;
- funcionar incluso sin conexión a Internet;
- utilizar distintos modelos de lenguaje sin depender de ninguno de ellos.

---

# Principios permanentes

Estas reglas deberán mantenerse durante toda la evolución del proyecto salvo que exista una decisión arquitectónica importante que justifique modificarlas.

El objetivo es que todas las decisiones futuras mantengan una visión coherente y consistente de Legna como compañera digital.