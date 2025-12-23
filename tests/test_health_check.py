import os
import sys


def _ensure_repo_in_path():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)


def test_check_health_success():
    _ensure_repo_in_path()
    from scripts.health_check import check_health

    class FakeLLM:
        def __call__(self, prompt: str):
            return "Hello from fake"

    res = check_health(model="fake-model", probe="Hi", llm=FakeLLM())
    assert res["ok"] is True
    assert res["model"] == "fake-model"
    assert "Hello from fake" in res["response_preview"]


def test_check_health_no_model(monkeypatch):
    _ensure_repo_in_path()
    from scripts.health_check import check_health

    # Ensure no env var is present for this test
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    res = check_health(model=None, probe="Hi", llm=None)
    assert res["ok"] is False
    assert "OLLAMA_MODEL not set" in res["error"]


def test_check_health_llm_error():
    _ensure_repo_in_path()
    from scripts.health_check import check_health

    class ErrorLLM:
        def __call__(self, prompt: str):
            raise RuntimeError("boom")

    res = check_health(model="fake-model", probe="Hi", llm=ErrorLLM())
    assert res["ok"] is False
    assert "boom" in res["error"]
