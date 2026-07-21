import requests
from tools.base import Tool

class HTTPRequestTool(Tool):
    def __init__(self):
        super().__init__(name="http_request", description="Realiza peticiones HTTP (GET, POST, etc.)")

    def execute(self, url, method="GET", data=None, headers=None):
        try:
            response = requests.request(method=method, url=url, json=data, headers=headers)
            return {
                "status_code": response.status_code,
                "content": response.text[:1000], # Limitamos contenido
                "headers": dict(response.headers)
            }
        except Exception as e:
            return f"Error en la petición: {str(e)}"

class DownloadFileTool(Tool):
    def __init__(self):
        super().__init__(name="download_url", description="Descarga un archivo desde una URL")

    def execute(self, url, dest_path):
        try:
            response = requests.get(url, stream=True)
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return f"Archivo descargado en: {dest_path}"
        except Exception as e:
            return f"Error en la descarga: {str(e)}"
