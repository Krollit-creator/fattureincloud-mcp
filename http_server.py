#!/usr/bin/env python3
"""HTTP transport wrapper for Fatture in Cloud MCP Server."""

import contextlib
import os

from mcp.server.sse import SseServerTransport
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.routing import Mount, Router

from server import app


# --- Streamable HTTP transport (raccomandato per Claude.ai Custom Connectors)
session_manager = StreamableHTTPSessionManager(
    app=app,
    event_store=None,
    json_response=False,
    stateless=True,
)


async def handle_streamable_http(scope, receive, send):
    await session_manager.handle_request(scope, receive, send)


# --- SSE transport (legacy, mantenuto come fallback)
sse_transport = SseServerTransport("/messages/")


async def handle_sse(scope, receive, send):
    async with sse_transport.connect_sse(scope, receive, send) as (r, w):
        await app.run(r, w, app.create_initialization_options())


@contextlib.asynccontextmanager
async def lifespan(_app):
    async with session_manager.run():
        yield


# Usiamo Router direttamente (non Starlette) per disabilitare redirect_slashes.
# Senza questo, GET /mcp -> 307 redirect to /mcp/, e Claude.ai non segue il redirect.
starlette_app = Router(
    routes=[
        Mount("/mcp", app=handle_streamable_http),
        Mount("/sse", app=handle_sse),
        Mount("/messages/", app=sse_transport.handle_post_message),
    ],
    redirect_slashes=False,
    lifespan=lifespan,
)


def main():
    import uvicorn
    uvicorn.run(
        starlette_app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        log_level="info",
    )


if __name__ == "__main__":
    main()
