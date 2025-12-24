"""Direct example showing how to call an Ollama chat model without LangChain."""

import os
import sys


def _require_model():
    from dotenv import load_dotenv
    load_dotenv()
    model = os.environ.get("OLLAMA_MODEL")
    if not model:
        raise RuntimeError(
            "OLLAMA_MODEL not set. Copy .env.example to .env and set "
            "OLLAMA_MODEL to your local Ollama model name."
        )
    return model

# Ensure local package import works when running examples directly
repo_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(repo_root, "src"))

try:
    import ollama
except Exception:
    print("Please install the 'ollama' python package: pip install ollama")
    raise

# Helper to extract assistant text when the client returns verbose objects
try:
    from langchain_ollama.ollama_wrapper import _extract_assistant_content
except Exception:
    # If local package isn't installed, attempt to add src/ and retry
    repo_root = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(repo_root, "src"))
    from langchain_ollama.ollama_wrapper import _extract_assistant_content


def _require_model():
    from dotenv import load_dotenv
    load_dotenv()
    model = os.environ.get("OLLAMA_MODEL")
    if not model:
        raise RuntimeError(
            "OLLAMA_MODEL not set. Copy .env.example to .env and set "
            "OLLAMA_MODEL to your local Ollama model name."
        )
    return model


def simple_chat(prompt: str) -> str:
    model = _require_model()
    # Try to use top-level client if available
    if hasattr(ollama, "chat"):
        resp = ollama.chat(model, messages=[{"role": "user", "content": prompt}])
        return str(_extract_assistant_content(resp))
    # Try client object
    if hasattr(ollama, "Ollama"):
        client = ollama.Ollama()
        if hasattr(client, "chat"):
            resp = client.chat(model, messages=[{"role": "user", "content": prompt}])
            return str(_extract_assistant_content(resp))
        if hasattr(client, "predict"):
            resp = client.predict(model, prompt)
            return str(_extract_assistant_content(resp))
    raise RuntimeError(
        "Could not find a compatible Ollama client API."
        " Consult README for supported versions."
    )


if __name__ == "__main__":
    try:
        _require_model()
    except RuntimeError as e:
        print(e)
        sys.exit(2)

    print("Direct Ollama chat demo. Type 'exit' to quit.")
    while True:
        prompt = input("User: ")
        if prompt.strip().lower() in ("exit", "quit"):
            break
        out = simple_chat(prompt)
        print("Model:", out)
