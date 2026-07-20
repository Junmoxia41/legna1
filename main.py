from ai.llm import LLMClient
from memory.manager import MemoryManager
from models.memory import Memory


print("========== LEGNA ==========\n")

memory = MemoryManager()


# ========================================================
# PRUEBA DE MEMORIA
# ========================================================

test_memory = Memory(

    memory_type="fact",

    category="test",

    content="Este es el primer recuerdo de Legna."

)

memory.save_memory(test_memory)

print("\n===== MEMORIES =====")

for memory_data in memory.load_memories():

    print(memory_data)


# ========================================================
# CHAT
# ========================================================

jarvis = LLMClient()

while True:

    mensaje = input("\nTú: ")

    if mensaje.lower() == "salir":
        break

    evaluations = memory.extract_knowledge(mensaje)

    print("\n===== MEMORY EVALUATIONS =====")

    if not evaluations:

        print("No se detectó información relevante.")

    else:

        for i, evaluation in enumerate(evaluations, start=1):

            print(f"\nEvaluación #{i}")
            print(f"Should Save: {evaluation.should_save}")
            print(f"Importance: {evaluation.importance}")
            print(f"Confidence: {evaluation.confidence}")
            print(f"Type: {evaluation.memory_type}")
            print(f"Category: {evaluation.category}")
            print(f"Canonical Key: {evaluation.canonical_key}")
            print(f"Content: {evaluation.content}")
            print(f"Reason: {evaluation.reason}")

    # ========================================================
    # PRUEBA OBSERVATIONS
    # ========================================================

    print("\n===== OBSERVATIONS =====")

    observations = memory.load_observations()

    if not observations:

        print("No hay observaciones.")

    else:

        for observation in observations:

            print(observation)

    # respuesta = jarvis.preguntar(mensaje)

    # print(f"\nLegna:\n{respuesta}")