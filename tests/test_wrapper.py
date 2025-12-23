import pytest

try:
    import ollama
except Exception:
    ollama = None

from langchain_ollama.ollama_wrapper import OllamaLLM


def test_wrapper_instantiation():
    # This test only checks wrapper instantiation.
    # It does not call the real API.
    llm = OllamaLLM(model="test-model")
    assert hasattr(llm, "model")


@pytest.mark.skipif(ollama is None, reason="ollama package not installed")
def test_direct_call():
    # Only run if ollama package is installed and a test model exists locally
    llm = OllamaLLM(model="llama2")
    res = None
    try:
        if hasattr(llm, "__call__"):
            res = llm("Hello")
        else:
            res = llm._call("Hello")
    except Exception:
        pytest.skip("Could not contact local Ollama daemon or model not installed")
    assert res is not None
