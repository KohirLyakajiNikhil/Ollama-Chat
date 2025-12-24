from dotenv import load_dotenv

load_dotenv()

import os
import sys

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Ollama Web Chat")

# Allow local browsers during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from examples/static and templates from examples/templates
app.mount("/static", StaticFiles(directory="examples/static"), name="static")
templates = Jinja2Templates(directory="examples/templates")


def _import_wrapper():
    try:
        from langchain_ollama.ollama_wrapper import OllamaLLM

        return OllamaLLM
    except Exception:
        repo_root = os.path.dirname(os.path.dirname(__file__))
        sys.path.insert(0, os.path.join(repo_root, "src"))
        from langchain_ollama.ollama_wrapper import OllamaLLM

        return OllamaLLM


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/chat")
async def chat_endpoint(req: Request):
    data = await req.json()
    msg = data.get("message", "")
    if not msg:
        return JSONResponse({"error": "empty message"}, status_code=400)

    model = os.environ.get("OLLAMA_MODEL")
    if not model:
        return JSONResponse({"error": "OLLAMA_MODEL not set"}, status_code=400)

    OllamaLLM = _import_wrapper()
    try:
        llm = OllamaLLM(model=model)
        # Use the LangChain-compatible API if present
        if hasattr(llm, "_call"):
            out = llm._call(msg)
        elif hasattr(llm, "generate_text"):
            out = llm.generate_text(msg)
        else:
            out = str(llm(msg))
        return JSONResponse({"reply": out})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
