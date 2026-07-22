"""Local runtime configuration. Environment variables override defaults."""
import os

LM_STUDIO_URL = os.getenv("LEGNA_LM_STUDIO_URL", "http://127.0.0.1:1234/v1/chat/completions")
LLAMA_CPP_URL = os.getenv("LEGNA_LLAMA_CPP_URL", "http://127.0.0.1:8080/v1/chat/completions")
MODEL = os.getenv("LEGNA_MODEL", "local-model")
