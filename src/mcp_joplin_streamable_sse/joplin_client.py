"""Async client for the Joplin Data API (Web Clipper)."""

from __future__ import annotations

from typing import Any

import httpx

from .errors import JoplinApiError


class JoplinClient:
    """Thin wrapper around Joplin's REST API."""

    def __init__(self, *, base_url: str, token: str, timeout_seconds: float = 15.0) -> None:
        self._token = token
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=httpx.Timeout(timeout_seconds),
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def request_json(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        method = method.upper()
        url_path = path if path.startswith("/") else f"/{path}"
        q = dict(params or {})
        q.setdefault("token", self._token)

        resp = await self._client.request(method, url_path, params=q, json=json_body)
        if resp.status_code >= 400:
            raise JoplinApiError(
                status_code=resp.status_code,
                method=method,
                url=str(resp.request.url),
                response_text=(resp.text or "").strip(),
            )

        # Joplin always returns JSON for API routes.
        data = resp.json()
        if not isinstance(data, dict):
            raise JoplinApiError(
                status_code=resp.status_code,
                method=method,
                url=str(resp.request.url),
                response_text=f"Unexpected JSON type: {type(data).__name__}",
            )
        return data

    async def get_paged(
        self,
        path: str,
        *,
        page: int = 1,
        limit: int = 20,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        q = dict(params or {})
        q.update({"page": page, "limit": limit})
        return await self.request_json("GET", path, params=q)
