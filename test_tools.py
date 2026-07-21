from assistant import LegnaAssistant

def test_modular_tools():
    print("========== PRUEBA DE HERRAMIENTAS MODULARES ==========\n")
    legna = LegnaAssistant()
    
    # 1. Listar herramientas disponibles
    print("Herramientas registradas:")
    tools = legna.memory_manager.tool_registry.list_all_tools()
    for cat, items in tools.items():
        print(f"  [{cat}]:")
        for name, desc in items.items():
            print(f"    - {name}: {desc}")

    # 2. Probar ejecución directa de una herramienta de archivo
    print("\n[Test] Creando un archivo de prueba...")
    result = legna.memory_manager.tool_registry.execute_tool(
        "create_file", 
        path="prueba_modular.txt", 
        content="Contenido generado por el sistema de herramientas modulares."
    )
    print(f"Resultado: {result}")

    # 3. Probar lectura
    print("\n[Test] Leyendo el archivo creado...")
    content = legna.memory_manager.tool_registry.execute_tool(
        "read_file", 
        path="prueba_modular.txt"
    )
    print(f"Contenido: {content}")

    # 4. Probar ejecución de comando de terminal (Simulado)
    print("\n[Test] Ejecutando comando de terminal (echo)...")
    cmd_result = legna.memory_manager.tool_registry.execute_tool(
        "execute_cmd", 
        command="echo 'Legna está operativa'"
    )
    print(f"Resultado CMD: {cmd_result.strip()}")

if __name__ == "__main__":
    test_modular_tools()
