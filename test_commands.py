from memory.manager import MemoryManager

def test_command_recognition():
    print("Iniciando prueba de reconocimiento de comandos...")
    memory = MemoryManager()
    
    # Prueba 1: Un comando conocido
    print("\n--- Test 1: 'abre la calculadora' ---")
    memory.extract_knowledge("abre la calculadora")
    
    # Prueba 2: Un hecho (para ver que conviven)
    print("\n--- Test 2: 'vivo en Madrid' ---")
    evals = memory.extract_knowledge("vivo en Madrid")
    for e in evals:
        if e.memory_type == "fact":
            print(f"Hecho detectado: {e.content}")

    # Prueba 3: Un alias
    print("\n--- Test 3: 'ejecuta el script' ---")
    memory.extract_knowledge("ejecuta el script")

if __name__ == "__main__":
    test_command_recognition()
