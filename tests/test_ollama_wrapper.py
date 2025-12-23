from unittest.mock import MagicMock, patch

import pytest

from langchain_ollama.ollama_wrapper import FROM_OLLAMA, OllamaClientError, OllamaLLM


def test_generate_text_with_mocked_client(monkeypatch):
    # If the ollama client exists, simulate a .chat function
    if FROM_OLLAMA:
        fake_resp = MagicMock()
        fake_resp.content = "Hello from Ollama"

        with patch(
            "langchain_ollama.ollama_wrapper.ollama.chat",
            return_value=fake_resp,
        ):
            llm = OllamaLLM(model="test-model")
            out = llm._call("Hi") if hasattr(llm, "_call") else llm.generate_text("Hi")
            assert "Hello from Ollama" in out


def test_cli_fallback_when_python_client_unavailable(monkeypatch):
    # Force the module to behave as if the `ollama` client is not present
    monkeypatch.setattr("langchain_ollama.ollama_wrapper.FROM_OLLAMA", False)

    # Mock shutil.which to pretend the CLI is present
    # and make subprocess.run return a simple Completed object
    def _fake_shutil_which(name):
        return "/usr/bin/ollama"

    monkeypatch.setattr(
        "langchain_ollama.ollama_wrapper.shutil.which",
        _fake_shutil_which,
    )

    class Completed:
        returncode = 0
        stdout = b"CLI response"
        stderr = b""

    monkeypatch.setattr(
        "langchain_ollama.ollama_wrapper.subprocess.run",
        lambda *a, **k: Completed(),
    )

    llm = OllamaLLM(model="test-model")
    out = llm._call("Hello") if hasattr(llm, "_call") else llm.generate_text("Hello")
    assert "CLI response" in out


def test_error_when_no_client_and_no_cli(monkeypatch):
    monkeypatch.setattr("langchain_ollama.ollama_wrapper.FROM_OLLAMA", False)
    monkeypatch.setattr(
        "langchain_ollama.ollama_wrapper.shutil.which",
        lambda name: None,
    )

    llm = OllamaLLM(model="test-model")
    with pytest.raises(OllamaClientError):
        _ = llm._call("Hi") if hasattr(llm, "_call") else llm.generate_text("Hi")
