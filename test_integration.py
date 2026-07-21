from assistant import LegnaAssistant

def test_full_integration():
    print("========== TEST DE INTEGRACIÓN FASE A & B ==========\n")
    legna = LegnaAssistant()
    
    # 1. Probar Sistema de Archivos Extendido
    print("\n[Archivo] Creando carpeta y buscando...")
    legna.memory_manager.tool_registry.execute_tool("create_folder", path="docs_test")
    legna.memory_manager.tool_registry.execute_tool("create_file", path="docs_test/info.txt", content="Datos importantes.")
    found = legna.memory_manager.tool_registry.execute_tool("search_file", pattern="info.txt", root_dir="docs_test")
    print(f"Búsqueda: {found}")

    # 2. Probar Documentos (JSON y Markdown)
    print("\n[Documentos] Creando JSON y Markdown...")
    legna.memory_manager.tool_registry.execute_tool("process_json", path="config.json", action="write", data={"version": "0.4", "status": "active"})
    legna.memory_manager.tool_registry.execute_tool("write_markdown", path="resumen.md", title="Resumen Biología", content="La célula es la unidad básica de la vida.")
    
    # 3. Probar Windows/Información del sistema
    print("\n[Windows] Obteniendo info del sistema...")
    sys_info = legna.memory_manager.tool_registry.execute_tool("system_info")
    print(f"Sistema: {sys_info['system']} {sys_info['release']}")

    # 4. Probar Python (Ejecutar script dinámico)
    print("\n[Python] Creando y ejecutando script dinámico...")
    legna.memory_manager.tool_registry.execute_tool("create_file", path="hello.py", content="print('Hola desde script dinámico de Legna')")
    py_result = legna.memory_manager.tool_registry.execute_tool("run_python", path="hello.py")
    print(f"Resultado Python: {py_result.strip()}")

if __name__ == "__main__":
    test_full_integration()
