from assistant import LegnaAssistant
import json

def run_complex_workflow_demo():
    print("========== DEMO DE WORKFLOW COMPLEJO DE LEGNA ==========\n")
    legna = LegnaAssistant()
    
    # Definimos un flujo de trabajo: 
    # 1. Obtener la hora.
    # 2. Crear un directorio de proyecto.
    # 3. Generar un archivo de configuración JSON.
    # 4. Crear un informe Markdown.
    # 5. Buscar los archivos creados.
    
    workflow_steps = [
        {
            "tool": "get_time",
            "args": {}
        },
        {
            "tool": "create_folder",
            "args": {"path": "proyecto_final_legna"}
        },
        {
            "tool": "process_json",
            "args": {
                "path": "proyecto_final_legna/config.json",
                "action": "write",
                "data": {
                    "proyecto": "Legna Core",
                    "estado": "Integración Completa",
                    "modulos": 16
                }
            }
        },
        {
            "tool": "write_markdown",
            "args": {
                "path": "proyecto_final_legna/README.md",
                "title": "Documentación del Proyecto",
                "content": "Este proyecto fue generado automáticamente por el sistema de automatización de Legna."
            }
        },
        {
            "tool": "search_file",
            "args": {"pattern": "*", "root_dir": "proyecto_final_legna"}
        }
    ]

    print("[Acción] Ejecutando workflow secuencial...")
    results = legna.memory_manager.tool_registry.execute_tool("run_workflow", steps=workflow_steps)
    
    print("\n========== RESULTADOS DEL WORKFLOW ==========")
    for i, res in enumerate(results, 1):
        tool_name = list(res.keys())[0]
        output = list(res.values())[0]
        print(f"Paso {i} [{tool_name}]: {output}")

    print("\n[Verificación] Leyendo el archivo JSON creado...")
    config_data = legna.memory_manager.tool_registry.execute_tool("process_json", path="proyecto_final_legna/config.json", action="read")
    print(f"Datos del JSON: {config_data}")

if __name__ == "__main__":
    run_complex_workflow_demo()
