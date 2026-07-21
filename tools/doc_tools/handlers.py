import json
from tools.base import Tool

class JSONTool(Tool):
    def __init__(self):
        super().__init__(name="process_json", description="Lee o escribe archivos JSON")

    def execute(self, path, action="read", data=None):
        try:
            if action == "read":
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            elif action == "write":
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                return f"JSON escrito en {path}"
        except Exception as e:
            return f"Error en JSON: {str(e)}"

class MarkdownTool(Tool):
    def __init__(self):
        super().__init__(name="write_markdown", description="Crea documentos Markdown estructurados")

    def execute(self, path, title, content):
        try:
            md_content = f"# {title}\n\n{content}"
            with open(path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            return f"Markdown creado en {path}"
        except Exception as e:
            return f"Error en Markdown: {str(e)}"
