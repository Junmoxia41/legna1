# ARCHITECTURE
## Proyecto Jarvis

Versión: 0.3

---

# Propósito

Este documento describe la arquitectura del proyecto Jarvis.

No pretende documentar cada clase ni cada línea de código.

Su objetivo es explicar las decisiones de diseño que definen cómo está construido Legna, por qué se tomaron dichas decisiones y cómo deberá evolucionar la arquitectura en el futuro.

---

# Filosofía General

Jarvis es el nombre del proyecto.

Legna será la inteligencia artificial.

Los modelos de lenguaje (Mistral u otros futuros) no representan la inteligencia de Legna.

Son únicamente motores de razonamiento.

La inteligencia de Legna deberá surgir de la cooperación entre distintos sistemas especializados.

Actualmente los pilares principales son:

- conocimiento;
- memoria;
- aprendizaje;
- contexto;
- identidad;
- planificación;
- automatización;
- proactividad.

El objetivo del proyecto no es construir un chatbot.

El objetivo es construir una compañera digital capaz de aprender y evolucionar con el tiempo.

---

# Principios Fundamentales

## Autonomía

Los módulos principales de Legna deben ser capaces de funcionar por sí mismos.

Los modelos de lenguaje actuarán únicamente como apoyo cuando aporten valor.

Nunca deberán convertirse en una dependencia obligatoria para el funcionamiento básico del sistema.

---

## Evolución gradual

La arquitectura siempre se diseñará pensando en el crecimiento.

Sin embargo, únicamente se implementará aquello que sea necesario en la fase actual.

Se evita la sobrearquitectura.

---

## Una responsabilidad por módulo

Cada módulo tendrá una única responsabilidad claramente definida.

Cuando una clase empiece a realizar varias tareas distintas deberá dividirse.

---

## Bajo acoplamiento

Los módulos deben conocerse lo mínimo posible.

Cada sistema deberá comunicarse mediante interfaces simples y modelos del dominio.

Ningún módulo deberá depender de la implementación interna de otro.

---

## Encapsulación

Cada módulo ocultará su implementación interna.

El resto del sistema únicamente utilizará su interfaz pública.

---

# Arquitectura General

La arquitectura actual está dividida en dos grandes sistemas independientes.

## Sistema de conocimiento

Responsable de comprender el lenguaje del usuario.

Flujo:

Usuario

↓

KnowledgeEngine

↓

DetectorRegistry

↓

Detectores especializados

↓

MemoryEvaluation

---

## Sistema de memoria

Responsable de aprender a partir del conocimiento obtenido.

Flujo previsto:

MemoryEvaluation

↓

Observation

↓

ShortTermMemory

↓

MemoryConsolidator

↓

Statistics

↓

Memory

↓

LongTermMemory

---

Ambos sistemas evolucionarán de forma independiente.

El sistema de conocimiento interpreta información.

El sistema de memoria decide qué hacer con ella.

---

## Sistema conversacional

Actualmente el sistema conversacional permanece separado.

Usuario

↓

LLMClient

↓

LM Studio

↓

Modelo de lenguaje

El modelo de lenguaje no participa directamente en la comprensión ni en la memoria.

Actúa únicamente como motor de razonamiento cuando sea necesario.

---

# Responsabilidad de cada módulo

## main.py

Es el punto de entrada del proyecto.

Su única responsabilidad consiste en iniciar y conectar todos los módulos del sistema.

No debe contener lógica de negocio.

---

## MemoryManager

Es el coordinador del sistema de memoria.

No interpreta lenguaje.

No almacena datos directamente.

No conoce SQLite.

Su responsabilidad consiste únicamente en coordinar los distintos módulos del sistema de memoria.

---

## KnowledgeEngine

Es el coordinador del sistema de conocimiento.

Su responsabilidad consiste en ejecutar los detectores registrados y unificar sus resultados.

Nunca almacena información.

Nunca interactúa con SQLite.

Nunca depende del modelo de lenguaje.

Devuelve una colección de objetos MemoryEvaluation.

---

## DetectorRegistry

Centraliza el registro de todos los detectores disponibles.

Permite ampliar el sistema simplemente registrando un nuevo detector.

KnowledgeEngine desconoce qué detectores existen.

Únicamente ejecuta los detectores registrados.

---

## Detectores

Cada detector posee una única responsabilidad.

Ejemplos actuales:

- PreferenceDetector
- FactDetector

Ejemplos futuros:

- GoalDetector
- HabitDetector
- TaskDetector
- EventDetector
- RelationshipDetector
- EmotionDetector
- ContradictionDetector

Todos los detectores:

- producen objetos MemoryEvaluation;
- no almacenan recuerdos;
- no conocen SQLite;
- no dependen unos de otros.

---

## TextExtractor

Es una utilidad compartida por todos los detectores.

Su responsabilidad consiste únicamente en limpiar y dividir texto.

No conoce preferencias.

No conoce hechos.

No toma decisiones.

Simplemente proporciona herramientas reutilizables para el procesamiento del lenguaje.

---

## Database

Es el responsable exclusivo de la persistencia.

Toda operación relacionada con SQLite deberá pasar por este módulo.

Ningún otro componente conocerá la implementación de la base de datos.

Su única responsabilidad consiste en almacenar y recuperar información.

---

## LLMClient

Responsable exclusivo de comunicarse con el modelo de lenguaje.

No almacena recuerdos.

No conoce SQLite.

No contiene lógica del sistema de memoria.

Puede sustituirse por cualquier otro proveedor de modelos sin modificar el resto del proyecto.

---

# Arquitectura de Memoria

La memoria de Legna se divide en distintas etapas.

Cada etapa representa una responsabilidad específica dentro del proceso de aprendizaje.

El objetivo es evitar que toda información detectada se convierta inmediatamente en un recuerdo permanente.

---

## Flujo general

Usuario

↓

KnowledgeEngine

↓

MemoryEvaluation

↓

Observation

↓

ShortTermMemory

↓

MemoryConsolidator

↓

Statistics

↓

Memory

↓

LongTermMemory

---

## Filosofía

Legna no aprende directamente de las conversaciones.

Primero observa.

Después acumula evidencia.

Más tarde decide.

Finalmente recuerda.

Este comportamiento intenta aproximarse al proceso natural de aprendizaje humano.

---

## Observation

Observation representa una única observación realizada por Legna.

No representa un recuerdo.

No representa una decisión.

Representa únicamente un hecho observado.

Se crea a partir de un objeto MemoryEvaluation.

Contiene información como:

- detector
- memory_type
- category
- content
- importance
- confidence
- persistencia
- polaridad
- timestamp

Observation no conoce SQLite.

No conoce ShortTermMemory.

No contiene lógica de negocio.

---

## ShortTermMemory

La memoria a corto plazo almacena observaciones temporales.

Su responsabilidad consiste únicamente en registrar observaciones.

No analiza información.

No consolida recuerdos.

No interpreta lenguaje.

Las observaciones permanecerán almacenadas únicamente durante el tiempo necesario para decidir si deben convertirse en recuerdos permanentes.

---

## MemoryConsolidator

Es el coordinador del aprendizaje.

Su responsabilidad consiste en decidir cuándo revisar la memoria a corto plazo.

No analiza directamente las observaciones.

Su función consiste únicamente en coordinar el proceso de consolidación.

---

## Statistics

Statistics analiza las observaciones almacenadas.

No guarda información.

No modifica recuerdos.

No interpreta lenguaje.

Actúa como un servicio de análisis.

Su responsabilidad consiste en calcular métricas como:

- frecuencia;
- repetición;
- importancia acumulada;
- confianza acumulada;
- persistencia.

A partir de estos resultados MemoryConsolidator decidirá si una observación merece convertirse en un recuerdo permanente.

---

## Memory

Memory representa un recuerdo consolidado.

Nunca se crea directamente a partir del usuario.

Siempre nace después del proceso de consolidación.

Contiene únicamente información persistente.

No contiene lógica de negocio.

---

## LongTermMemory

Representa el almacenamiento permanente de recuerdos.

Su contenido será utilizado posteriormente durante la recuperación de contexto y la conversación.

---

## History

History representa el historial de los recuerdos.

No almacena observaciones.

No participa en el aprendizaje.

Su función consiste en registrar eventos importantes relacionados con los recuerdos.

Ejemplos:

- creación;
- actualización;
- consolidación;
- eliminación;
- restauración.

Este sistema permitirá auditar la evolución de la memoria de Legna.

---

## Papelera

Los recuerdos eliminados manualmente no serán destruidos inmediatamente.

Pasarán primero a una papelera temporal.

Después de un periodo de seguridad podrán eliminarse definitivamente.

Este comportamiento permitirá recuperar recuerdos eliminados por error.

---

# Base de datos

Actualmente el proyecto utiliza una única base de datos.

database/

    memory.db

Esta base contendrá progresivamente tablas como:

- memories
- observations
- conversations
- metadata

En el futuro podrán añadirse:

- history
- trash

Toda operación de persistencia será responsabilidad exclusiva del módulo Database.

---

# Modelos del dominio

Legna utiliza modelos propios para representar conceptos del dominio.

Actualmente existen:

## Memory

Representa un recuerdo permanente.

---

## MemoryEvaluation

Representa el resultado producido por un detector.

No representa una memoria.

No representa una observación.

Representa únicamente la evaluación realizada por el sistema de conocimiento.

---

## Observation

Representa una observación temporal.

Constituye el puente entre el sistema de conocimiento y el sistema de memoria.

---

# Separación entre lógica y conocimiento

La arquitectura diferencia claramente dos conceptos.

Lógica.

Conocimiento.

Los módulos contienen únicamente lógica.

Los archivos de configuración contienen conocimiento.

Ejemplo:

KnowledgeEngine

↓

Lógica de coordinación.

language.py

↓

Patrones lingüísticos.

TextExtractor

↓

Utilidades generales de procesamiento de texto.

Los detectores contienen únicamente lógica relacionada con su responsabilidad.

El conocimiento utilizado por los detectores deberá permanecer separado de su implementación.

---

# Evolución futura

La arquitectura continuará creciendo mediante módulos independientes.

Entre los sistemas previstos se encuentran:

- Identity
- Planner
- Goal Manager
- Automation
- Context Engine
- Security
- Initiative

Todos ellos deberán seguir los mismos principios definidos en este documento:

- autonomía;
- responsabilidad única;
- bajo acoplamiento;
- encapsulación;
- evolución gradual.

---

# Filosofía de desarrollo

La arquitectura siempre tendrá prioridad sobre la implementación.

Antes de añadir una nueva funcionalidad deberá definirse claramente:

- qué responsabilidad tendrá;
- cómo interactuará con el resto del sistema;
- qué dependencias tendrá;
- cómo podrá evolucionar.

La implementación será siempre una consecuencia del diseño.

Nunca al contrario.

Los detectores no deciden qué recordar.

Únicamente aportan evidencia.

El sistema de memoria será el responsable de aprender a partir de esa evidencia.

Si una limpieza de texto puede alterar el significado de una observación, dicha limpieza no deberá realizarse mediante reglas simples.

Los módulos del dominio no deberán comunicarse directamente cuando exista la posibilidad de que un mismo evento pueda interesar a varios sistemas. En futuras versiones, esta comunicación evolucionará hacia un sistema interno de eventos (Event Bus), manteniendo el desacoplamiento entre los distintos componentes de Legna. Durante las primeras versiones, esta comunicación podrá realizarse mediante llamadas directas para mantener la simplicidad del sistema.

Las ideas relacionadas con Perception, Attention, World Model avanzado, Entity-Centric Model y Event Bus forman parte de la visión futura del proyecto, pero no se implementarán hasta que exista una necesidad real.