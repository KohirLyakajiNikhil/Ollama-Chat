

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from fastapi import FastAPI, Request, Depends, Cookie
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from uuid import uuid4
from typing import Dict, List, Tuple

load_dotenv()

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

# In-memory store for chat history per session (for demo; not for production)
user_histories: Dict[str, List[Tuple[str, str]]] = {}


def _import_wrapper():
    # Import OllamaLLM from the wrapper
    from langchain_ollama.ollama_wrapper import OllamaLLM
    return OllamaLLM

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/chat")
async def chat_endpoint(
    req: Request,
    response: Response,
    session_id: str = Cookie(default=None, alias="session_id")
):
    data = await req.json()
    msg = data.get("message", "")
    if not msg:
        return JSONResponse({"error": "empty message"}, status_code=400)

    # Assign a session id if not present
    if not session_id:
        session_id = str(uuid4())
        response.set_cookie(key="session_id", value=session_id)

    # Get or create history for this session
    history = user_histories.setdefault(session_id, [])
    history.append(("user", msg))

    model = os.environ.get("OLLAMA_MODEL")
    if not model:
        return JSONResponse({"error": "OLLAMA_MODEL not set"}, status_code=400)

    OllamaLLM = _import_wrapper()
    try:
        llm = OllamaLLM(model=model, base_url=os.environ.get("OLLAMA_BASE_URL"))
        # Use conversation history for context
        prompt_text = "\n".join([
            f"User: {u}\nAssistant: {a}" if a else f"User: {u}"
            for u, a in history if u == "user" or a
        ])
        out = llm(prompt_text)
        history.append(("assistant", out))
        return JSONResponse({"reply": out})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
