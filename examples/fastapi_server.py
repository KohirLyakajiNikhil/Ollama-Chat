"""Simple FastAPI server exposing a chat endpoint backed by Ollama (via wrapper).

Run:
    uvicorn examples.fastapi_server:app --reload
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from langchain_ollama.ollama_wrapper import OllamaLLM

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
                "OLLAMA_MODEL not set. Copy .env.example to .env and set OLLAMA_MODEL to your model name."
            )
        llm = OllamaLLM(model=MODEL)
    return llm


class Message(BaseModel):
    text: str


@app.post("/chat")
async def chat(msg: Message):
    # The wrapper exposes a simple interface; it may be an LLM object or callable
    if hasattr(llm, "__call__"):
        text = llm(msg.text)
    elif hasattr(llm, "generate_text"):
        text = llm.generate_text(msg.text)
    else:
        # try to call generate via LangChain API
        try:
            text = llm._call(msg.text)
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
        if hasattr(llm, "__call__"):
            out = llm(probe)
        elif hasattr(llm, "generate_text"):
            out = llm.generate_text(probe)
        else:
            out = llm._call(probe)
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
