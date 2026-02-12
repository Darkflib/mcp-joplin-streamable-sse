from __future__ import annotations

from mcp_joplin_sse.settings import Settings


def test_settings_load_from_env(monkeypatch) -> None:
    monkeypatch.setenv("JOPLIN_TOKEN", "t")
    monkeypatch.setenv("MCP_API_KEY", "k")
    s = Settings()
    assert s.joplin_token == "t"
    assert s.mcp_api_key == "k"
