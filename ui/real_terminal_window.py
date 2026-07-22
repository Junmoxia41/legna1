import webview

def create_terminal_window():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Legna Terminal Real</title>
        <style>
            body { background:#05060A; color:#00FF9F; font-family: monospace; padding:20px; }
            #output { white-space: pre-wrap; height: 400px; overflow-y: auto; }
            input { width:100%; background:#0A0B10; color:#00FF9F; border:none; padding:10px; font-family:monospace; }
        </style>
    </head>
    <body>
        <h3>Legna Terminal Real</h3>
        <div id="output">> Terminal lista. Escribe comandos.\n</div>
        <input id="cmd" placeholder="Escribe comando..." onkeydown="if(event.key==='Enter') runCommand()">
        <script>
            function runCommand() {
                const input = document.getElementById('cmd');
                const output = document.getElementById('output');
                const cmd = input.value.trim();
                if (!cmd) return;
                
                output.innerText += `> ${cmd}\n`;
                input.value = '';
                
                // Llamar a Python para ejecutar comando real
                window.pywebview.api.execute_command(cmd).then(result => {
                    output.innerText += result + '\\n';
                    output.scrollTop = output.scrollHeight;
                });
            }
        </script>
    </body>
    </html>
    """
    window = webview.create_window("Legna Terminal Real", html=html, width=900, height=600)
    webview.start()