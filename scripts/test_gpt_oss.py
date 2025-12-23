#!/usr/bin/env python
"""One-off script to test the Ollama wrapper with a specific local model."""
import os
import sys

from dotenv import load_dotenv

# Load environment variables from .env at repository root (optional)
load_dotenv()

# Ensure local package import works
repo_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(repo_root, "src"))

MODEL = os.environ.get("OLLAMA_MODEL", "gpt-oss:latest")
print("Using MODEL=", MODEL)

try:
    from langchain_ollama.ollama_wrapper import OllamaLLM
except Exception:
    print("Could not import Ollama wrapper")
    raise

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
