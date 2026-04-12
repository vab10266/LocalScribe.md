# config.py
from pathlib import Path

MAX_TOOL_CALLS = 10
TIMEOUT_SECONDS = 10

VAULT_PATH = "vault"
MARQO_INDEX_NAME = "markdown-notes"

LLM_MODEL_PATH = Path("~/models/llama-3.1-8b.gguf").expanduser()
EMBEDDING_MODEL = "nomic-embed-text"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

WELCOME_MESSAGE = "Hello there."


from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
