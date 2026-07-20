import requests

from config import LM_STUDIO_URL
from config import MODEL


class LLMClient:

    def __init__(self):

        self.url = LM_STUDIO_URL
        self.model = MODEL

        print("Cliente LLM creado.")

    def preguntar(self, mensaje):

        datos = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": mensaje
                }
            ]
        }

        try:

            respuesta = requests.post(
                self.url,
                json=datos,
                timeout=60
            )

            respuesta.raise_for_status()

            datos = respuesta.json()

            return datos["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException:

            return "No puedo comunicarme con LM Studio."

        except Exception as e:

            return f"Error: {e}"