"""Direct example showing how to call an Ollama chat model without LangChain."""

import os

from dotenv import load_dotenv

# Load environment variables from .env at repository root (optional)
load_dotenv()

try:
    import ollama
except Exception:
    print("Please install the 'ollama' python package: pip install ollama")
    raise

MODEL = os.environ.get("OLLAMA_MODEL")


def _require_model():
    if not MODEL:
        raise RuntimeError(
            "OLLAMA_MODEL not set. Copy .env.example to .env and set OLLAMA_MODEL to your local Ollama model name."
        )


def simple_chat(prompt: str) -> str:
    # Try to use top-level client if available
    if hasattr(ollama, "chat"):
        resp = ollama.chat(MODEL, messages=[{"role": "user", "content": prompt}])
        return getattr(resp, "content", resp)

    # Try client object
    if hasattr(ollama, "Ollama"):
        client = ollama.Ollama()
        if hasattr(client, "chat"):
            resp = client.chat(MODEL, messages=[{"role": "user", "content": prompt}])
            return (
                resp.get("content")
                if isinstance(resp, dict)
                else getattr(resp, "content", resp)
            )
        if hasattr(client, "predict"):
            resp = client.predict(MODEL, prompt)
            return getattr(resp, "content", resp)

    raise RuntimeError(
        "Could not find a compatible Ollama client API."
        " Consult README for supported versions."
    )


if __name__ == "__main__":
    print("Direct Ollama chat demo. Type 'exit' to quit.")
    while True:
        prompt = input("User: ")
        if prompt.strip().lower() in ("exit", "quit"):
            break
        out = simple_chat(prompt)
        print("Model:", out)
