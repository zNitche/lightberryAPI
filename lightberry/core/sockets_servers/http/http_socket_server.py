import asyncio
import time
from lightberry.utils import common_utils
from lightberry.core.communication.request import Request
from lightberry.utils import requests_utils

from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Type, Coroutine, Callable
    from lightberry.config.base_config import BaseConfig
    from asyncio import StreamReader, StreamWriter


class HttpSocketServer:
    def __init__(self,
                 host="0.0.0.0",
                 port=80,
                 debug_mode=False):
        self.server_task: Coroutine | None = None

        self.debug_mode = debug_mode
        self.config: Type[BaseConfig] | None = None

        self.host = host
        self.port = port

    async def __load_request(self, request_stream: StreamReader) -> Request | None:
        try:
            request_header_string = await requests_utils.load_request_header_from_stream(request_stream)
            self.__print_debug(f"request header string: {request_header_string}")

            request = Request()
            request.parse_header(request_header_string)

            if request.content_length:
                request_body_string = await request_stream.readexactly(request.content_length)
                request.parse_body(request_body_string.decode())

            self.__print_debug(f"request body string: {request.body}")

            return request

        except Exception as e:
            self.__print_debug(f"error while parsing request", exception=e)
            return None

    async def __requests_handler(self, client_r: StreamReader, client_w: StreamWriter):
        raise NotImplementedError("Not implemented")

    async def __debug_requests_handler_wrapper(self, client_r: StreamReader, client_w: StreamWriter):
        self.__print_debug(f"connection from: {client_w.get_extra_info('peername')}")
        start_time = time.ticks_ms() if self.debug_mode else None

        await self.__requests_handler(client_r, client_w)

        self.__print_debug(f"request took: {time.ticks_ms() - start_time}ms")

    def __get_requests_handler_for_mode(self) -> Callable[[StreamReader, StreamWriter], Coroutine]:
        return self.__debug_requests_handler_wrapper if self.debug_mode else self.__requests_handler

    def setup(self):
        handler = self.__get_requests_handler_for_mode()
        self.server_task = asyncio.start_server(handler, self.host, self.port)

    def __print_debug(self, message: str, exception: Exception | None = None):
        common_utils.print_debug(message, f"SERVER - {self.__class__.__name__}",
                                 debug_enabled=self.debug_mode, exception=exception)
