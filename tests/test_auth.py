from __future__ import annotations

from starlette.testclient import TestClient

from mcp_joplin_sse.asgi import create_app


def test_requires_api_key(monkeypatch) -> None:
    monkeypatch.setenv("JOPLIN_TOKEN", "t")
    monkeypatch.setenv("MCP_API_KEY", "k")
    app = create_app()
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 401

    r2 = client.get("/health", headers={"x-api-key": "k"})
    assert r2.status_code == 200
    assert r2.json() == {"ok": True}
