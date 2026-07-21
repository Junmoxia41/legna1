import requests
import os
from tools.base import Tool

class GithubAPITool(Tool):
    def __init__(self):
        super().__init__(name="github_api", description="Interacciona con la API de GitHub (requiere GITHUB_TOKEN)")

    def execute(self, endpoint, method="GET", data=None):
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            return "Error: GITHUB_TOKEN no configurado en variables de entorno."
        
        url = f"https://api.github.com/{endpoint}"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        try:
            response = requests.request(method=method, url=url, json=data, headers=headers)
            return response.json()
        except Exception as e:
            return f"Error en API GitHub: {str(e)}"
