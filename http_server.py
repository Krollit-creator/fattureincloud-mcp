#!/usr/bin/env python3
"""HTTP transport wrapper for Fatture in Cloud MCP Server.

Espone il server MCP via HTTP per il deployment remoto (Railway, Docker, ecc.).
Per uso locale via stdio, avviare invece `server.py` direttamente.

Vengono esposti DUE endpoint per massima compatibilita' con i client MCP:
  - POST/GET /mcp        -> Streamable HTTP transport (raccomandato, usato da
                            Claude.ai Custom Connectors)
  - GET      /sse        -> SSE transport (compatibilita' legacy)
  - POST     /messages/  -> endpoint POST per i messaggi del transport SSE

Variabili d'ambiente lette:
- PORT       : porta di ascolto (default: 8000, Railway la imposta automaticamente)
- HOST       : host di bind (default: 0.0.0.0)

Le credenziali Fatture in Cloud (FIC_ACCESS_TOKEN, FIC_COMPANY_ID, FIC_SENDER_EMAIL)
sono lette da server.py al momento dell'import.
"""

import contextlib
import os

from mcp.server.sse import SseServerTransport
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Mount

# Importa l'istanza Server gia' configurata da server.py.
# In questo modo non duplichiamo logica e il fork rimane allineato con l'upstream.
from server import app


# ---------------------------------------------------------------------------
# Streamable HTTP transport (transport raccomandato per i client MCP moderni)
# ---------------------------------------------------------------------------
# Stateless mode: ogni richiesta e' indipendente, niente affinita' di sessione.
# Adatto al deployment su Railway dove il container puo' essere ricreato.
session_manager = StreamableHTTPSessionManager(
    app=app,
    event_store=None,
    json_response=False,
    stateless=True,
)


async def handle_streamable_http(scope, receive, send):
    """ASGI handler per le richieste MCP via Streamable HTTP."""
    await session_manager.handle_request(scope, receive, send)


# ---------------------------------------------------------------------------
# SSE transport (legacy, mantenuto per compatibilita' con vecchi client)
# ---------------------------------------------------------------------------
sse_transport = SseServerTransport("/messages/")


async def handle_sse(scope, receive, send):
    """ASGI handler per la connessione SSE (transport legacy)."""
    async with sse_transport.connect_sse(scope, receive, send) as (
        read_stream,
        write_stream,
    ):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


# ---------------------------------------------------------------------------
# Lifespan: avvia/ferma il session manager dello Streamable HTTP
# ---------------------------------------------------------------------------
@contextlib.asynccontextmanager
async def lifespan(_starlette_app):
    """Gestisce il ciclo di vita del session manager Streamable HTTP."""
    async with session_manager.run():
        yield


# ---------------------------------------------------------------------------
# Applicazione Starlette
# ---------------------------------------------------------------------------
starlette_app = Starlette(
    routes=[
        # Streamable HTTP - endpoint moderno (raccomandato)
        Mount("/mcp", app=handle_streamable_http),
        # SSE - endpoint legacy
        Mount("/sse", app=handle_sse),
        Mount("/messages/", app=sse_transport.handle_post_message),
    ],
    lifespan=lifespan,
)


def main():
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run(
        starlette_app,
        host=host,
        port=port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
