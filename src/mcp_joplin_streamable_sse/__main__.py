"""CLI entrypoint."""

from __future__ import annotations

import uvicorn

from .asgi import create_app
from .settings import Settings


def main() -> None:
    settings = Settings()
    uvicorn.run(
        create_app(),
        host=settings.mcp_host,
        port=settings.mcp_port,
        log_level="info",
    )
