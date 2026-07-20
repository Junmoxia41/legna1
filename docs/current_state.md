CURRENT_STATE
Proyecto Jarvis

Versión: 0.3

Estado actual

Actualmente el sistema de conocimiento se considera funcional en su primera versión.

Legna ya es capaz de detectar distintos tipos de conocimiento utilizando detectores especializados y generar evaluaciones independientes del sistema de memoria.

El siguiente objetivo consiste en construir el sistema de aprendizaje.

Sistemas completados
Arquitectura
KnowledgeEngine.
DetectorRegistry.
Detectores independientes.
TextExtractor.
language.py.
Database.
MemoryManager.
Memory.
MemoryEvaluation.
Detectores implementados

Actualmente existen:

PreferenceDetector.
FactDetector.

Ambos utilizan:

TextExtractor.
language.py.
MemoryEvaluation.

Los detectores producen evaluaciones.

No almacenan recuerdos.

No conocen SQLite.

No dependen unos de otros.

Flujo actual
Usuario

↓

KnowledgeEngine

↓

MemoryEvaluation

Actualmente el flujo termina aquí.

Todavía no existe aprendizaje.

Próxima etapa

La siguiente fase consiste en construir el sistema de memoria.

El objetivo es que Legna deje de limitarse a detectar información y comience a aprender de ella.

Arquitectura aprobada

El flujo aprobado para el aprendizaje es:

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
Observation

Estado:

Diseño aprobado.

Implementación iniciada.

Responsabilidad:

Representar una única observación realizada por Legna.

Observation nace a partir de MemoryEvaluation.

No representa un recuerdo.

No contiene lógica.

No conoce SQLite.

No conoce la memoria.

ShortTermMemory

Estado:

Diseño aprobado.

Implementación iniciada.

Responsabilidad:

Almacenar observaciones temporales.

No analiza información.

No interpreta lenguaje.

No decide qué recordar.

Su única responsabilidad consiste en registrar observaciones hasta que el sistema decida consolidarlas o descartarlas.

Statistics

Estado:

Diseño aprobado.

No implementado.

Responsabilidad:

Analizar las observaciones almacenadas.

Calcular:

frecuencia;
importancia acumulada;
confianza acumulada;
persistencia;
repeticiones.

No almacena datos.

No modifica recuerdos.

Actúa únicamente como servicio de análisis.

MemoryConsolidator

Estado:

Diseño aprobado.

No implementado.

Responsabilidad:

Coordinar el proceso de consolidación.

Solicita información a Statistics.

Decide cuándo una observación merece convertirse en un recuerdo permanente.

No interpreta lenguaje.

LongTermMemory

Estado:

Existe el modelo Memory.

Existe persistencia básica.

Pendiente:

Integración con el sistema de consolidación.

History

Estado:

Idea aprobada.

No implementado.

Responsabilidad:

Registrar la historia de los recuerdos.

No participa en el aprendizaje.

Registrará eventos como:

creación;
consolidación;
actualización;
eliminación;
restauración.
Trash

Estado:

Idea aprobada.

No implementado.

Los recuerdos eliminados manualmente pasarán primero a una papelera temporal antes de su eliminación definitiva.

Decisiones arquitectónicas recientes

Durante esta etapa se aprobaron las siguientes decisiones:

Separar completamente el Sistema de Conocimiento del Sistema de Memoria.
Sustituir MemoryEvaluator por KnowledgeEngine.
Utilizar detectores especializados.
Crear Observation como nuevo modelo del dominio.
Utilizar ShortTermMemory como memoria temporal.
Utilizar Statistics únicamente como servicio de análisis.
Crear MemoryConsolidator para coordinar el aprendizaje.
Mantener Database como único responsable de la persistencia.
Mantener History separado del proceso de aprendizaje.
Próximos pasos inmediatos
Finalizar Observation.
Finalizar ShortTermMemory.
Crear la tabla observations.
Implementar save_observation().
Implementar load_observations().
Integrar ShortTermMemory con MemoryManager.
Verificar que las observaciones se almacenan correctamente.
Comenzar el desarrollo de Statistics.
Objetivo de la siguiente sesión

Conseguir que una frase como:

"Me gusta la pizza."

genere automáticamente:

MemoryEvaluation

↓

Observation

↓

SQLite (observations)

Ese será el primer paso para que Legna comience a aprender de forma autónoma.

Mi recomendación

Yo guardaría este documento junto a los otros tres:

docs/

architecture.md
roadmap.md
rulebook.md
current_state.md

Porque cumple una función distinta: es el punto de reanudación del proyecto. Cada vez que abras un chat nuevo, bastará con leer este archivo para saber exactamente en qué punto estaba Legna, qué decisiones ya están tomadas y cuál es el siguiente paso, sin tener que reconstruir semanas de conversaciones. Creo que, a partir de ahora, será uno de los documentos más útiles del proyecto