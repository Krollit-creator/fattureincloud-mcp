#!/usr/bin/env python3
"""HTTP transport wrapper for Fatture in Cloud MCP Server."""

import contextlib
import os

from mcp.server.sse import SseServerTransport
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

from server import app


# --- Streamable HTTP transport (raccomandato per Claude.ai Custom Connectors)
session_manager = StreamableHTTPSessionManager(
    app=app,
    event_store=None,
    json_response=False,
    stateless=True,
)


# --- SSE transport (legacy, mantenuto come fallback)
sse_transport = SseServerTransport("/messages/")


async def _send_404(send):
    await send({
        "type": "http.response.start",
        "status": 404,
        "headers": [(b"content-type", b"text/plain; charset=utf-8")],
    })
    await send({"type": "http.response.body", "body": b"Not Found"})


async def asgi_app(scope, receive, send):
    """Dispatcher ASGI custom.

    Gestisce sia /mcp che /mcp/ per Streamable HTTP, perche' Claude.ai
    sembra normalizzare il path strippando lo slash finale.
    """
    scope_type = scope.get("type")

    if scope_type == "lifespan":
        async with session_manager.run():
            while True:
                msg = await receive()
                if msg["type"] == "lifespan.startup":
                    await send({"type": "lifespan.startup.complete"})
                elif msg["type"] == "lifespan.shutdown":
                    await send({"type": "lifespan.shutdown.complete"})
                    return
        return

    if scope_type != "http":
        return

    path = scope.get("path", "")

    # Streamable HTTP: accetta /mcp e /mcp/ (e qualsiasi sub-path)
    if path == "/mcp" or path.startswith("/mcp/"):
        # Normalizza /mcp -> /mcp/ per il session_manager
        if path == "/mcp":
            scope = {**scope, "path": "/mcp/", "raw_path": b"/mcp/"}
        await session_manager.handle_request(scope, receive, send)
        return

    # SSE legacy: GET /sse apre la connessione
    if path == "/sse" or path.startswith("/sse/"):
        async with sse_transport.connect_sse(scope, receive, send) as (r, w):
            await app.run(r, w, app.create_initialization_options())
        return

    # SSE legacy: POST /messages/ riceve i messaggi
    if path.startswith("/messages/"):
        await sse_transport.handle_post_message(scope, receive, send)
        return

    # Tutto il resto -> 404
    await _send_404(send)


def main():
    import uvicorn
    uvicorn.run(
        asgi_app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        log_level="info",
    )


if __name__ == "__main__":
    main()
