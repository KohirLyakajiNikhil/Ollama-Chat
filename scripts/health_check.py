#!/usr/bin/env python
"""Simple health check for configured Ollama model.

This script attempts a lightweight prompt to the model and reports status as JSON.
"""
import json
import os
import sys
import traceback
from typing import Any, Dict, Optional

from dotenv import load_dotenv

load_dotenv()


def check_health(
    model: Optional[str] = None,
    probe: Optional[str] = None,
    llm: Any = None,
) -> Dict[str, Any]:
    """Check the configured model and return a dict with the result.

    - model: override the model name (default reads from OLLAMA_MODEL)
    - probe: override the probe prompt
    - llm: optionally provide an already-constructed LLM object (for testing)
    """
    model = model or os.environ.get("OLLAMA_MODEL", "")
    if not model:
        return {"ok": False, "error": "OLLAMA_MODEL not set"}

    probe = probe or os.environ.get("OLLAMA_HEALTH_PROMPT", "Say hi in one sentence.")

    # If an llm is injected (for tests), use it directly
    if llm is None:
        # Ensure the repository package path is importable
        repo_root = os.path.dirname(os.path.dirname(__file__))
        sys.path.insert(0, os.path.join(repo_root, "src"))

        try:
            from langchain_ollama.ollama_wrapper import (
                OllamaLLM,
            )
        except Exception as e:  # pragma: no cover - import-time failures
            err_msg = "Cannot import wrapper: " + str(e)
            return {"ok": False, "error": err_msg}

        llm = OllamaLLM(model=model)

    try:
        if hasattr(llm, "__call__"):
            out = llm(probe)
        else:
            out = llm._call(probe)

        if isinstance(out, str) and len(out) < 300:
            preview = out
        elif isinstance(out, str):
            preview = out[:300] + "..."
        else:
            preview = str(type(out))

        return {"ok": True, "model": model, "response_preview": preview}

    except Exception as e:
        # Distinguish Ollama-specific client errors when possible
        err = str(e)
        tb = traceback.format_exc()
        return {"ok": False, "model": model, "error": err, "trace": tb}


if __name__ == "__main__":
    res = check_health()
    print(json.dumps(res))
    if res.get("ok"):
        sys.exit(0)
    sys.exit(3)
