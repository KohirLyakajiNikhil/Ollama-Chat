"""Example showing a minimal LangChain integration using the Ollama wrapper.

This example attempts to use LangChain's LLM base class wrapper defined in
`src/langchain_ollama/ollama_wrapper.py`. Depending on your LangChain version,
this may work out-of-the-box or require small API adjustments.
"""

import importlib
import os
import sys

# Ensure local package import works when running examples directly
repo_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(repo_root, "src"))

from dotenv import load_dotenv

# Import the local package lazily inside the example function so example scripts
# can be run directly without requiring an editable install. This avoids modifying
# sys.path at module import time and prevents flake8 E402 errors.

# LangChain import compatibility across versions — do not raise on failure.
HAVE_LANGCHAIN = False
LLMChain = None
PromptTemplate = None
_lc_import_errors = []

# Try multiple import locations for LLMChain and PromptTemplate using importlib

for name, attr in [
    ("langchain.chains", "LLMChain"),
    ("langchain", "LLMChain"),
]:
    try:
        mod = importlib.import_module(name)
        LLMChain = getattr(mod, attr)
        HAVE_LANGCHAIN = True
        break
    except Exception as exc:
        _lc_import_errors.append(exc)
        LLMChain = None

for name, attr in [
    ("langchain.prompts", "PromptTemplate"),
    ("langchain", "PromptTemplate"),
]:
    try:
        mod = importlib.import_module(name)
        PromptTemplate = getattr(mod, attr)
        HAVE_LANGCHAIN = True
        break
    except Exception as exc:
        _lc_import_errors.append(exc)
        PromptTemplate = None

# Load environment variables from .env at repository root (optional)
load_dotenv()

MODEL = os.environ.get("OLLAMA_MODEL")


def run_example():
    if not MODEL:
        print(
            "OLLAMA_MODEL is not set. Copy .env.example to .env and set "
            "OLLAMA_MODEL to your model name, then re-run this example."
        )
        return

    # Import locally so running examples directly works without an editable
    # install. If the import fails, add `src/` to sys.path and retry once.
    try:
        from langchain_ollama.ollama_wrapper import OllamaLLM
    except Exception:
        repo_root = os.path.dirname(os.path.dirname(__file__))
        sys.path.insert(0, os.path.join(repo_root, "src"))
        from langchain_ollama.ollama_wrapper import OllamaLLM

    llm = OllamaLLM(model=MODEL)

    # If LangChain's LLM base isn't available, fall back to a simple loop that
    # calls the Ollama wrapper directly (it is callable and returns text).
    if "HAVE_LANGCHAIN" in globals() and HAVE_LANGCHAIN:
        prompt = PromptTemplate.from_template(
            "You are a helpful assistant. User: {input}"
        )
        chain = LLMChain(llm=llm, prompt=prompt)

        def _run_input(text: str) -> str:
            return chain.run(text)

    else:
        print(
            "LangChain's LLMChain/PromptTemplate not available — "
            "falling back to direct OllamaLLM calls.\n"
            "Install a compatible 'langchain' to use this example with LLMChain, "
            "or use 'examples/chat_direct.py'."
        )

        def _run_input(text: str) -> str:
            # OllamaLLM implements __call__ and returns generated text
            return llm(text)

    while True:
        user_input = input("User: ")
        if user_input.strip().lower() in ("exit", "quit"):
            break
        out = _run_input(user_input)
        print("Model:", out)


if __name__ == "__main__":
    run_example()
