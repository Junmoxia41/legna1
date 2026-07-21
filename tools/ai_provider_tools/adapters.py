import requests
import os
from tools.base import Tool

class OpenAIAdapterTool(Tool):
    def __init__(self):
        super().__init__(name="openai_chat", description="Consulta a OpenAI (requiere OPENAI_API_KEY)")

    def execute(self, prompt, model="gpt-3.5-turbo"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key: return "Error: API Key no encontrada."
        
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}"}
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}]
            }
            response = requests.post(url, json=payload, headers=headers)
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Error en OpenAI: {str(e)}"

class AnthropicAdapterTool(Tool):
    def __init__(self):
        super().__init__(name="anthropic_chat", description="Consulta a Anthropic (requiere ANTHROPIC_API_KEY)")

    def execute(self, prompt, model="claude-3-haiku-20240307"):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key: return "Error: API Key no encontrada."
        
        try:
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            payload = {
                "model": model,
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}]
            }
            response = requests.post(url, json=payload, headers=headers)
            return response.json()['content'][0]['text']
        except Exception as e:
            return f"Error en Anthropic: {str(e)}"
