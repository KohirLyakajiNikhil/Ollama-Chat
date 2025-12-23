from fastapi.testclient import TestClient

import examples.fastapi_server as server


def _ensure_repo_in_path():
    import os
    import sys

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)


# Ensure the repo root is importable when tests run.
# Calling this at import time may not be ideal on some test runners.
_ensure_repo_in_path()


class FakeLLM:
    def __call__(self, prompt: str):
        return "Hello from fake"


def test_fastapi_health_success(monkeypatch):
    # Inject fake llm into the server module
    monkeypatch.setattr(server, "llm", FakeLLM())
    client = TestClient(server.app)
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert "Hello from fake" in data["response_preview"]


def test_fastapi_health_failure(monkeypatch):
    class ErrorLLM:
        def __call__(self, prompt: str):
            raise RuntimeError("boom")

    monkeypatch.setattr(server, "llm", ErrorLLM())
    client = TestClient(server.app)
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is False
    assert "boom" in data["error"]
