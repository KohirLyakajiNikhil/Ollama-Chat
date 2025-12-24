![CI](https://github.com/KohirLyakajiNikhil/Ollama-Chat/actions/workflows/ci.yml/badge.svg?branch=main)


# LangChain + Ollama Chat Demo ✅
## 🖥️ Web Application (Browser Chat UI)

You can chat with your local Ollama model in your browser using the included web app.


### Prerequisites

#### 1. Install Ollama

- **Ubuntu:**
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  # Start the Ollama service
  ollama serve &
  # Pull a model (example: llama2)
  ollama pull llama2
  ```

- **Windows:**
  1. Download the Windows installer from: https://ollama.com/download
  2. Run the installer and follow the prompts.
  3. Open a new terminal and run:
     ```powershell
     ollama serve
     # Pull a model (example: llama2)
     ollama pull llama2
     ```

#### 2. Install Python and Create a Virtual Environment

- **Ubuntu:**
  ```bash
  sudo apt update
  sudo apt install python3 python3-venv python3-pip -y
  python3 -m venv .venv
  source .venv/bin/activate
  ```

- **Windows (PowerShell):**
  ```powershell
  # Ensure Python 3.10+ is installed (https://www.python.org/downloads/)
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  # If you see a script execution error, run:
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
  .\.venv\Scripts\Activate.ps1
  ```

---

### Quick Start

1. **Install dependencies** (see above for venv instructions):
  ```bash
  pip install -r requirements.txt
  python -m pip install -e .  # recommended for local dev
  ```

2. **Set your model** in `.env` or as an environment variable:
  ```ini
  OLLAMA_MODEL=your_model_name
  ```
  Example: `OLLAMA_MODEL=llama2` or any model you have installed in Ollama.

3. **Run the web app:**
  ```bash
  uvicorn examples.web_app:app --reload
  ```
  Then open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

  - The chat UI supports avatars, message bubbles, a typing indicator, and works on desktop/mobile.
  - If you see an error about `jinja2` missing, install it with `pip install jinja2`.

4. **Troubleshooting:**
  - Make sure the Ollama daemon is running and the model is installed.
  - If you get a model error, check your `.env` or environment variable for `OLLAMA_MODEL`.
  - For best results, use a smaller or quantized model if you have limited RAM.

---

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
# (Optional for local development) Install the package in editable mode so examples
# can import the local package without adjusting PYTHONPATH:
python -m pip install -e .
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

### Other Examples

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


---

## Health check
- Use `scripts/health_check.py` to verify that the configured model (from `.env` or the `OLLAMA_MODEL` env var) is reachable and responding to a short probe. Example:

  python scripts/health_check.py

- FastAPI example exposes a `/health` GET endpoint that returns a JSON object with `ok: true` when the model responds and `ok: false` with an error message if it does not. Example:

  uvicorn examples.fastapi_server:app --reload
  # Then visit http://127.0.0.1:8000/health

---

## Known issues / model guidance
- Large models (for example `gpt-oss:latest`) may require substantially more RAM than typical desktop machines (e.g., >12 GB). If a model fails to load, try a smaller model, a quantized variant, or verify the model health first with `python scripts/health_check.py`.
- Ollama's CLI and Python client APIs can vary between releases; if you encounter API errors, check `src/langchain_ollama/ollama_wrapper.py` for compatibility workarounds.

---

## Contributions
- PRs welcome: add more robust LangChain chat model implementations, FastAPI demo, or tests.

## License
- MIT
