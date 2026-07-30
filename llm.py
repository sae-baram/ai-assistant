import os
from langchain_ollama import ChatOllama
from dotenv import load_dotenv


load_dotenv()

def get_llm():
    """Return the default LLM"""
    model_name = os.getenv("LLM_MODEL", "qwen2.5-coder:7b")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    return ChatOllama(
        model=model_name,
        base_url=base_url,
        temperature=0
    )