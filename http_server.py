#!/usr/bin/env python3
"""HTTP/SSE transport wrapper for Fatture in Cloud MCP Server.

Espone il server MCP via HTTP/SSE per il deployment remoto (Railway, Docker, ecc.).
Per uso locale via stdio, avviare invece `server.py` direttamente.

Variabili d'ambiente lette:
- PORT       : porta di ascolto (default: 8000, Railway la imposta automaticamente)
- HOST       : host di bind (default: 0.0.0.0)

Le credenziali Fatture in Cloud (FIC_ACCESS_TOKEN, FIC_COMPANY_ID, FIC_SENDER_EMAIL)
sono lette da server.py al momento dell'import.
"""

import os

from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount

# Importa l'istanza Server gia' configurata da server.py.
# In questo modo non duplichiamo logica e il fork rimane allineato con l'upstream.
from server import app


sse_transport = SseServerTransport("/messages/")


async def handle_sse(scope, receive, send):
    """ASGI handler per la connessione SSE in entrata da un client MCP (es. Claude.ai).

    Usiamo un handler ASGI puro (scope/receive/send) montato via Mount invece
    di un endpoint Starlette, perche' SSE non ritorna una Response normale
    ma tiene la connessione aperta per tutta la durata della sessione MCP.
    """
    async with sse_transport.connect_sse(scope, receive, send) as (
        read_stream,
        write_stream,
    ):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


# Applicazione Starlette: due endpoint
#  - GET  /sse        -> apre la connessione SSE (ASGI app montata)
#  - POST /messages/  -> riceve i messaggi MCP dal client
starlette_app = Starlette(
    routes=[
        Mount("/sse", app=handle_sse),
        Mount("/messages/", app=sse_transport.handle_post_message),
    ],
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
