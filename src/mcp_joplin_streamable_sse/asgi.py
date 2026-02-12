"""ASGI app hosting the MCP Streamable HTTP endpoint."""

from __future__ import annotations

import contextlib
import secrets
from collections.abc import AsyncIterator, Awaitable, Callable

from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from .mcp_server import create_mcp_server
from .settings import Settings


class ApiKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Starlette, *, api_key: str) -> None:
        super().__init__(app)
        self._api_key = api_key

    @staticmethod
    def _bypass_auth(path: str) -> bool:
        # Allow unauthenticated health checks and OAuth discovery probes.
        # Some MCP clients probe these endpoints before sending custom headers.
        if path == "/health":
            return True
        if path.startswith("/.well-known/"):
            return True
        return False

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if self._bypass_auth(request.url.path):
            return await call_next(request)
        presented = request.headers.get("x-api-key")
        if not presented or not secrets.compare_digest(presented, self._api_key):
            return JSONResponse({"error": "unauthorized"}, status_code=401)
        return await call_next(request)


async def health(_: Request) -> Response:
    return JSONResponse({"ok": True})


def create_app() -> Starlette:
    settings = Settings()
    mcp = create_mcp_server(settings)

    @contextlib.asynccontextmanager
    async def lifespan(_: Starlette) -> AsyncIterator[None]:
        # Streamable HTTP transport uses a session manager.
        async with mcp.session_manager.run():
            yield

    app = Starlette(
        routes=[
            Route("/health", endpoint=health, methods=["GET"]),
        ],
        lifespan=lifespan,
    )

    # Mount MCP at /mcp (default for streamable-http when mounted at /).
    app.mount("/", mcp.streamable_http_app())
    app.add_middleware(ApiKeyMiddleware, api_key=settings.mcp_api_key)
    return app
