import webview
from pathlib import Path

def create_monaco_window(file_path=None):
    """Crea una ventana con Monaco Editor"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>LegnaCode - Monaco Editor</title>
        <style>
            body {{ margin:0; background:#0A0B10; color:#E0E6ED; }}
            #container {{ height:100vh; width:100%; }}
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs/editor/editor.main.min.css">
    </head>
    <body>
        <div id="container"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs/loader.min.js"></script>
        <script>
            require.config({{ paths: {{ 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs' }} }});
            require(['vs/editor/editor.main'], function() {{
                monaco.editor.create(document.getElementById('container'), {{
                    value: '// Bienvenido a LegnaCode\\n// Syntax highlighting activado',
                    language: 'python',
                    theme: 'vs-dark',
                    automaticLayout: true,
                    fontSize: 14
                }});
            }});
        </script>
    </body>
    </html>
    """
    window = webview.create_window(
        "LegnaCode - Monaco Editor",
        html=html,
        width=1200,
        height=800
    )
    webview.start()