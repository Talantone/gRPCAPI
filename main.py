import asyncio
import contextvars
from typing import Optional, cast
from config.config import APP_PORT, APP_ADDR
from grpclib.events import RecvRequest, listen
from grpclib.server import Server
from grpclib.utils import graceful_exit

from db.base import initiate_database
from db_service import DBService

XRequestId = Optional[str]

request_id: contextvars.ContextVar[XRequestId] = \
    contextvars.ContextVar('x-request-id')


async def on_recv_request(event: RecvRequest) -> None:
    r_id = cast(XRequestId, event.metadata.get('x-request-id'))
    request_id.set(r_id)


async def serve(*, host: str, port: int) -> None:
    server = Server([DBService()])
    listen(server, RecvRequest, on_recv_request)
    with graceful_exit([server]):
        await server.start(host, port)
        print(f'Serving on {host}:{port}')
        await server.wait_closed()


if __name__ == '__main__':

    loop = asyncio.new_event_loop()
    loop.run_until_complete(initiate_database())
    loop.run_until_complete(serve(host=APP_ADDR, port=APP_PORT))
