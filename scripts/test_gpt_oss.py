#!/usr/bin/env python
"""One-off script to test the Ollama wrapper with a specific local model.

This script is intentionally named as a demo and not a pytest test so
it won't be collected by pytest during test discovery. Run it manually:

    python scripts/gpt_oss_demo.py
"""
import os
import sys

from dotenv import load_dotenv

# Load environment variables from .env at repository root (optional)
load_dotenv()

# Ensure local package import works
repo_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(repo_root, "src"))

MODEL = os.environ.get("OLLAMA_MODEL")
print("Using MODEL=", MODEL)


if __name__ == "__main__":
    if not MODEL:
        print(
            "OLLAMA_MODEL is not set. Copy .env.example to .env and set "
            "OLLAMA_MODEL to your model name, then re-run this demo."
        )
        sys.exit(2)

try:
    from langchain_ollama.ollama_wrapper import OllamaLLM
except Exception:
    print("Could not import Ollama wrapper")
    raise

if __name__ == "__main__":
    llm = OllamaLLM(model=MODEL)
    print("HAS_CALL" if hasattr(llm, "__call__") else "NO_CALL")
    try:
        if hasattr(llm, "__call__"):
            out = llm("Say hello in one sentence.")
        else:
            out = llm._call("Say hello in one sentence.")
        print("OUTPUT_START")
        print(out)
        print("OUTPUT_END")
    except Exception:
        print("CALL FAILED:")
        import traceback

        traceback.print_exc()
        raise
