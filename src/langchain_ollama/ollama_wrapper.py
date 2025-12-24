"""Enhanced wrapper for local Ollama chat models.

Provides a LangChain-friendly interface and a CLI fallback when the
`ollama` Python client isn't available.

Features:
- Threaded async support for sync clients
- Compact API compatible with `LLM` base classes (when available)
"""

import asyncio
import json
import re
import shlex
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional

try:
    # LangChain LLM base class (wrap to multiple lines to satisfy flake8)
    from langchain.llms.base import (
        LLM
    )

    LC_HAS_LLM = True
except Exception:
    LC_HAS_LLM = False

try:
    import ollama

    FROM_OLLAMA = True
except Exception:
    FROM_OLLAMA = False


class OllamaClientError(RuntimeError):
    pass


def _extract_assistant_content(resp: Any) -> str:
    """Extract the assistant reply text from various response shapes.

    Handles strings, dicts, objects with attributes, lists of messages,
    and simple CLI / repr fallbacks. Returns a plain text string.
    """
    # Direct string
    if isinstance(resp, str):
        return resp.strip()

    # dict-like responses
    if isinstance(resp, dict):
        # Common shapes:
        # - {'content': '...'}
        # - {'message': {...}}
        # - {'messages': [...]}
        # - {'choices': [...]}
        if "content" in resp and isinstance(resp["content"], str):
            return resp["content"].strip()
        if "message" in resp:
            return _extract_assistant_content(resp["message"])
        if "messages" in resp and isinstance(resp["messages"], (list, tuple)):
            for m in resp["messages"]:
                if isinstance(m, dict):
                    if m.get("role") == "assistant" and "content" in m:
                        return m["content"].strip()
            # fallback to first message content
            first = resp["messages"][0]
            return _extract_assistant_content(first)
        if "choices" in resp and isinstance(resp["choices"], (list, tuple)):
            choice = resp["choices"][0]
            if isinstance(choice, dict):
                if "message" in choice:
                    return _extract_assistant_content(choice["message"])
                if "text" in choice:
                    return str(choice["text"]).strip()

    # object-like responses
    # Try common attributes
    for attr in ("content", "message", "messages", "choices", "text"):
        try:
            if hasattr(resp, attr):
                val = getattr(resp, attr)
                # If it's a string-like
                if isinstance(val, str):
                    return val.strip()
                # If it's dict or list-like, recurse
                return _extract_assistant_content(val)
        except Exception:
            pass

    # Fallback: try to stringify and parse common patterns like
    # "message=Message(role='assistant', content='Hello', ...)"
    try:
        s = str(resp)
        # Try to find content='...'
        m = re.search(r"content=\'([^']+)\'", s)
        if m:
            return m.group(1).strip()
        m2 = re.search(r'"content"\s*:\s*"([^"]+)"', s)
        if m2:
            return m2.group(1).strip()
        # As a last resort return the string
        return s.strip()
    except Exception:
        return ""


def _call_ollama_cli(model: str, prompt: str, timeout: int = 30) -> str:
    """Fallback to calling the `ollama` CLI if the Python client is unavailable.

    We try `ollama chat` first, then fall back to older or alternate
    CLI commands such as `ollama generate` or `ollama run`.

    The CLI output parsing is tolerant: it returns stdout (str) when
    no structured output is available.
    """
    if not shutil.which("ollama"):
        raise OllamaClientError(
            "`ollama` CLI not found on PATH; install Ollama or install "
            "the Python client `ollama`."
        )

    # Try `ollama chat` which typically accepts --model and --prompt
    # or positional args depending on CLI version. We call a generic
    # command and return stdout. Adjust if your CLI supports JSON.
    cmd = f"ollama chat {shlex.quote(model)} --prompt {shlex.quote(prompt)}"
    try:
        completed = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        if completed.returncode != 0:
            # If chat failed, try `ollama generate` (older/newer CLI variations)
            cmd2 = (
                f"ollama generate {shlex.quote(model)} --prompt {shlex.quote(prompt)}"
            )
            completed2 = subprocess.run(
                cmd2,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                check=False,
            )
            if completed2.returncode == 0:
                out = completed2.stdout.decode(errors="ignore").strip()
                # Try to parse structured output
                try:
                    return _extract_assistant_content(json.loads(out))
                except Exception:
                    return out
            # If generate also failed, try `ollama run MODEL PROMPT`.
            # Some CLI versions accept the model and a prompt positionally.
            cmd3 = "ollama run " + shlex.quote(model) + " " + shlex.quote(prompt)
            completed3 = subprocess.run(
                cmd3,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                check=False,
            )
            if completed3.returncode == 0:
                out = completed3.stdout.decode(errors="ignore").strip()
                try:
                    return _extract_assistant_content(json.loads(out))
                except Exception:
                    return _extract_assistant_content(out)
            else:
                err = (
                    completed.stderr.decode(errors="ignore")
                    + "\n"
                    + completed2.stderr.decode(errors="ignore")
                    + "\n"
                    + completed3.stderr.decode(errors="ignore")
                )
                raise OllamaClientError(f"`ollama` CLI failed: {err.strip()}")
        out = completed.stdout.decode(errors="ignore").strip()
        try:
            return _extract_assistant_content(json.loads(out))
        except Exception:
            return _extract_assistant_content(out)
    except subprocess.TimeoutExpired as e:
        raise OllamaClientError(f"`ollama` CLI timed out: {e}")


async def _run_in_executor(fn, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        ThreadPoolExecutor(max_workers=1), lambda: fn(*args, **kwargs)
    )


if LC_HAS_LLM:

    class OllamaLLM(LLM):
        """LangChain-compatible LLM wrapper for Ollama.

        Parameters:
            model: name of the local Ollama model (e.g., `llama2`)
            base_url: unused placeholder for HTTP-based clients
            ollama_kwargs: dict forwarded to the Python client where
                supported (for example: temperature, system messages)
        """

        model: str
        base_url: Optional[str] = None
        ollama_kwargs: Dict[str, Any] = None

        def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
            # Prefer the Python client if available
            if FROM_OLLAMA:
                try:
                    if hasattr(ollama, "chat"):
                        resp = ollama.chat(
                            self.model,
                            messages=[{"role": "user", "content": prompt}],
                            **(self.ollama_kwargs or {}),
                        )
                        return getattr(resp, "content", resp)
                    elif hasattr(ollama, "Ollama"):
                        client = ollama.Ollama()
                        if hasattr(client, "chat"):
                            resp = client.chat(
                                self.model,
                                messages=[{"role": "user", "content": prompt}],
                                **(self.ollama_kwargs or {}),
                            )
                            return (
                                resp.get("content")
                                if isinstance(resp, dict)
                                else getattr(resp, "content", resp)
                            )
                        elif hasattr(client, "predict"):
                            resp = client.predict(
                                self.model, prompt, **(self.ollama_kwargs or {})
                            )
                            return getattr(resp, "content", resp)
                        else:
                            # fall through to CLI fallback
                            pass
                except Exception as e:
                    # try CLI fallback
                    try:
                        return _call_ollama_cli(self.model, prompt)
                    except Exception:
                        raise OllamaClientError(
                            f"Error using Ollama Python client: {e}"
                        )

            # Fallback to CLI
            return _call_ollama_cli(self.model, prompt)

        async def _acall(self, prompt: str, stop: Optional[List[str]] = None) -> str:
            # Run the blocking call in a thread to avoid blocking the event loop
            return await _run_in_executor(self._call, prompt, stop)

        @property
        def _identifying_params(self) -> Dict[str, Any]:
            return {"model": self.model}

        @property
        def _llm_type(self) -> str:
            return "ollama"

else:

    class OllamaLLM:
        """Fallback minimal wrapper when LangChain LLM base is not present.

        It supports synchronous `generate_text` and is callable.
        """

        def __init__(self, model: str, base_url: Optional[str] = None, **ollama_kwargs):
            self.model = model
            self.base_url = base_url
            self.ollama_kwargs = ollama_kwargs

        def generate_text(self, prompt: str) -> str:
            # Try the Python client
            if FROM_OLLAMA:
                try:
                    if hasattr(ollama, "chat"):
                        resp = ollama.chat(
                            self.model,
                            messages=[{"role": "user", "content": prompt}],
                            **(self.ollama_kwargs or {}),
                        )
                        return getattr(resp, "content", resp)
                    elif hasattr(ollama, "Ollama"):
                        client = ollama.Ollama()
                        if hasattr(client, "chat"):
                            resp = client.chat(
                                self.model,
                                messages=[{"role": "user", "content": prompt}],
                                **(self.ollama_kwargs or {}),
                            )
                            return (
                                resp.get("content")
                                if isinstance(resp, dict)
                                else getattr(resp, "content", resp)
                            )
                        elif hasattr(client, "predict"):
                            resp = client.predict(
                                self.model, prompt, **(self.ollama_kwargs or {})
                            )
                            return getattr(resp, "content", resp)
                except Exception:
                    # Fallthrough to CLI fallback
                    pass

            # CLI fallback
            return _call_ollama_cli(self.model, prompt)

        async def agenerate_text(self, prompt: str) -> str:
            return await _run_in_executor(self.generate_text, prompt)

        def __call__(self, prompt: str) -> str:
            return self.generate_text(prompt)
