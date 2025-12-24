![CI](https://github.com/KohirLyakajiNikhil/Ollama-Chat/actions/workflows/ci.yml/badge.svg?branch=main)

# LangChain + Ollama Example

This repository demonstrates how to use locally installed Ollama models with LangChain.

Key contents
- `src/langchain_ollama/ollama_wrapper.py` — LangChain-compatible `OllamaLLM` wrapper with Python client and CLI fallbacks.
- `examples/run_chat.py` — Convenience script that runs a quick direct and LangChain example.
- `examples/chat_direct.py` — Direct usage example invoking the `OllamaLLM` wrapper interactively.
- `examples/langchain_chat.py` — Example showing a minimal LangChain integration using the wrapper.
- `examples/fastapi_server.py` — FastAPI example exposing a `/health` endpoint to probe model availability.
- `tests/` — pytest tests that mock the Ollama client and the CLI fallback.

Quickstart
1. Install Ollama on your PC and set up a local model (see https://ollama.ai).
2. Create a virtual environment and install dependencies:

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt

3. Run the example:

    python examples/run_chat.py

Development
- Install dev dependencies and enable pre-commit:

    pip install -r requirements-dev.txt
    pre-commit install
    pre-commit run --all-files

Running tests (locally or in CI):

    pytest -q

Contributing
- See `CONTRIBUTING.md` for contribution guidelines.

License
- This project is MIT licensed — see `LICENSE`.
