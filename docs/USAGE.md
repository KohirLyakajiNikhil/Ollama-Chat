# Usage

## Quickstart
1. Install Ollama on your machine and pull or create a local model (see https://ollama.ai).
2. Create a virtual environment and install dependencies:

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt

3. Run example:

    python examples/run_chat.py

## Running tests

This repository includes pytest-based tests under `tests/`.

Install developer dependencies and run tests:

    pip install pytest
    pytest -q

If tests cannot run in this environment, add a CI workflow (GitHub Actions) that runs tests on push.

## Notes
- The `OllamaLLM` wrapper will try to use the `ollama` Python client when available and will fall back to calling the `ollama` CLI.
- If you run into compatibility issues with your installed LangChain version, adapt the wrapper to the local LangChain `LLM` base class implementation.

## Continuous Integration ✅
This repository includes a GitHub Actions workflow at `.github/workflows/ci.yml` which runs `pytest` on push and pull requests to `main` using multiple Python versions.
Make sure your `requirements.txt` (or other dependency manifest) is present at the repository root so the workflow installs your project's dependencies.
