![CI](https://github.com/KohirLyakajiNikhil/Ollama-Chat/actions/workflows/ci.yml/badge.svg?branch=main)

# LangChain + Ollama Chat Demo ✅

This repository contains a small Python project that demonstrates how to use chat models installed in Ollama locally from a LangChain application.

Highlights
- Direct example using the `ollama` Python client: `examples/chat_direct.py` 🔧
- LangChain example using a minimal wrapper: `examples/langchain_chat.py` 💡
- A lightweight wrapper is provided in `src/langchain_ollama/ollama_wrapper.py` ✅

Quick start
1. Install Ollama on your machine (https://ollama.com/docs). Ensure the Ollama daemon is running and you have pulled/installed a chat-capable model (e.g. `llama2`, `vicuna`, etc.).
2. Clone this repo and create a Python environment, then install dependencies:

```bash
python -m venv .venv
# Windows PowerShell (dot-source to activate)
. .venv\Scripts\Activate.ps1
# If PowerShell blocks script execution, allow it for the current session:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
# Windows CMD (legacy):
# .venv\Scripts\activate
# Git Bash / WSL:
# source .venv/bin/activate
pip install -r requirements.txt
```

Quick check: run `python -c "import sys; print(sys.prefix)"` — it should show the `.venv` path when the venv is active.

3. Set the model name you installed:

```bash
set OLLAMA_MODEL=llama2   # Windows PowerShell: $env:OLLAMA_MODEL = "llama2"
```

Alternatively, create a `.env` file at the repository root and add your preferred model there. The examples automatically load `.env` if present.

Example `.env` contents:

```ini
OLLAMA_MODEL=llama2
```

(Use PowerShell to change the value for your session, or edit `.env` to persist your preferred model.)

Bootstrap helper scripts

- A convenience script is provided to create the venv (if missing) and install requirements into it:
  - PowerShell: `scripts\bootstrap.ps1` — run `.\scripts\bootstrap.ps1` or `powershell -File .\scripts\bootstrap.ps1` (you may want to allow script execution for the session first as described above)
  - Bash (WSL / Git Bash / macOS / Linux): `scripts/bootstrap.sh` — run `./scripts/bootstrap.sh` (add `--dev` to also install dev requirements)

Preflight check

- Use `scripts/check_env.py` to verify required packages are present in the active Python environment:

```bash
python scripts/check_env.py
```

It prints a JSON object listing any missing packages and a tip to run `python -m pip install -r requirements.txt` in the active venv.

4. Run the direct chat example:

```bash
python examples/chat_direct.py
```

5. Run the LangChain example (may require a compatible LangChain version):

```bash
python examples/langchain_chat.py
```

Notes and troubleshooting
- The Ollama Python client API has changed across versions. If the examples fail with an API error, check `src/langchain_ollama/ollama_wrapper.py` and adjust the calls to your current `ollama` package's API (common methods are `ollama.chat`, `Ollama().chat`, or `Ollama().predict`).
- If LangChain's base classes change across versions, the wrapper may need slight adjustments. The wrapper includes a fallback minimal wrapper if the LangChain LLM base isn't detected.

Activation troubleshooting (PowerShell / CMD / Bash)

If you see errors when activating the virtualenv on Windows, try the commands below depending on your shell.

- PowerShell (recommended): dot-source the activation script (note the leading dot+space):

```powershell
. .venv\Scripts\Activate.ps1
```

- If PowerShell blocks script execution, allow it for the current session (no admin required):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
# Then re-run:
. .venv\Scripts\Activate.ps1
```

- If you prefer a one-off bypass (runs the script in a new PowerShell process):

```powershell
powershell -ExecutionPolicy Bypass -File .venv\Scripts\Activate.ps1
```

- CMD (legacy Windows shell):

```cmd
.venv\Scripts\activate
```

- Git Bash / WSL (Unix-like shells):

```bash
source .venv/bin/activate
```

Common error and fix

- Error: `.venv\Scripts\activate: The module '.venv' could not be loaded. For more information, run 'Import-Module .venv'.`
  - Cause: you ran the CMD activation script in PowerShell without dot-sourcing. PowerShell tried to treat `.venv\Scripts\activate` as a module import.
  - Fix: use the PowerShell form `. .venv\Scripts\Activate.ps1` (dot + space) instead.

- Error: `The script cannot be loaded because running scripts is disabled on this system.`
  - Fix: run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` and re-run the activation command above.

Quick verification

- After activation, confirm the venv is active with:

```bash
python -c "import sys; print(sys.prefix)"
```

It should show the path to the `.venv` folder.

Health check
- Use `scripts/health_check.py` to verify that the configured model (from `.env` or the `OLLAMA_MODEL` env var) is reachable and responding to a short probe. Example:

```
python scripts/health_check.py
```

- FastAPI example now exposes a `/health` GET endpoint that returns a JSON object with `ok: true` when the model responds and `ok: false` with an error message if it does not. Example:

```
uvicorn examples.fastapi_server:app --reload
# Then visit http://127.0.0.1:8000/health
```# Known issues / model guidance
- Large models (for example `gpt-oss:latest`) may require substantially more RAM than typical desktop machines (e.g., >12 GB). If a model fails to load, try a smaller model, a quantized variant, or verify the model health first with `python scripts/health_check.py`.
- Ollama's CLI and Python client APIs can vary between releases; if you encounter API errors, check `src/langchain_ollama/ollama_wrapper.py` for compatibility workarounds.
Contributions
- PRs welcome: add more robust LangChain chat model implementations, FastAPI demo, or tests.

License
- MIT
