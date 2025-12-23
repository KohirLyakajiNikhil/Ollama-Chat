![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg?branch=main)

# LangChain + Ollama Example

This repository demonstrates how to use locally installed Ollama models with LangChain.

Key contents
- `src/langchain_ollama/ollama_wrapper.py` — LangChain-compatible `OllamaLLM` wrapper with Python client and CLI fallbacks.
- `examples/run_chat.py` — Minimal examples for direct usage and LangChain integration.
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
