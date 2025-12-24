"""Simple FastAPI server exposing a chat endpoint backed by Ollama (via wrapper).

Run:
    uvicorn examples.fastapi_server:app --reload
"""

import os
import sys

# Ensure local package import works when running examples directly
repo_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(repo_root, "src"))

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

# Import local `langchain_ollama` lazily inside `_get_llm()` to avoid modifying
# sys.path at module import time and to keep flake8 happy.

# Load environment variables from .env at repository root (optional)
load_dotenv()

app = FastAPI()
MODEL = os.environ.get("OLLAMA_MODEL")
llm = None


def _get_llm():
    global llm
    if llm is None:
        if not MODEL:
            raise RuntimeError(
                "OLLAMA_MODEL not set. Copy .env.example to .env and set "
                "OLLAMA_MODEL to your model name."
            )
        # Import lazily and retry once if necessary so examples work without an
        # editable install.
        try:
            from langchain_ollama.ollama_wrapper import OllamaLLM
        except Exception:
            repo_root = os.path.dirname(os.path.dirname(__file__))
            sys.path.insert(0, os.path.join(repo_root, "src"))
            from langchain_ollama.ollama_wrapper import OllamaLLM

        llm = OllamaLLM(model=MODEL)
    return llm


class Message(BaseModel):
    text: str


@app.post("/chat")
async def chat(msg: Message):
    # The wrapper exposes a simple interface; it may be an LLM object or callable
    try:
        local_llm = _get_llm()
    except RuntimeError as e:
        return {"error": str(e)}

    if hasattr(local_llm, "__call__"):
        text = local_llm(msg.text)
    elif hasattr(local_llm, "generate_text"):
        text = local_llm.generate_text(msg.text)
    else:
        # try to call generate via LangChain API
        try:
            text = local_llm._call(msg.text)
        except Exception as e:
            return {"error": str(e)}
    return {"reply": text}


@app.get("/health")
async def health():
    """Lightweight health check for the configured model.

    Returns JSON with ok=True if the model responds to a brief probe prompt.
    """
    probe = os.environ.get("OLLAMA_HEALTH_PROMPT", "Say hi in one sentence.")
    try:
        local_llm = _get_llm()
    except RuntimeError as e:
        return {"ok": False, "model": MODEL, "error": str(e)}

    try:
        if hasattr(local_llm, "__call__"):
            out = local_llm(probe)
        elif hasattr(local_llm, "generate_text"):
            out = local_llm.generate_text(probe)
        else:
            out = local_llm._call(probe)
        return {
            "ok": True,
            "model": MODEL,
            "response_preview": (
                out
                if isinstance(out, str) and len(out) < 300
                else (out[:300] + "..." if isinstance(out, str) else str(type(out)))
            ),
        }
    except Exception as e:
        return {"ok": False, "model": MODEL, "error": str(e)}
