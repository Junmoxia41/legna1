import webbrowser
from tools.base import Tool

class OpenBrowserTool(Tool):
    def __init__(self):
        super().__init__(name="open_url", description="Abre una URL en el navegador predeterminado")

    def execute(self, url):
        try:
            webbrowser.open(url)
            return f"Abriendo: {url}"
        except Exception as e:
            return f"Error al abrir navegador: {str(e)}"

class SimpleScraperTool(Tool):
    def __init__(self):
        super().__init__(name="web_scrape", description="Extrae el texto de una página web")

    def execute(self, url):
        try:
            import requests
            from bs4 import BeautifulSoup
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Limpiamos scripts y estilos
            for script in soup(["script", "style"]):
                script.decompose()
            return soup.get_text(separator=' ', strip=True)[:2000]
        except Exception as e:
            return f"Error al extraer datos: {str(e)}"
