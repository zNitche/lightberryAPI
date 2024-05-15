from lightberry.config import ServerConfig as Config
from lightberry.core.communication.response import Response
from lightberry.core.sockets_servers.http import HttpSocketServer
from lightberry.utils import requests_utils
import asyncio

from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncio import StreamReader, StreamWriter


class SslProxyServer(HttpSocketServer):
    def __init__(self, wlan, host="0.0.0.0", port=Config.SERVER_PORT, debug_mode=Config.DEBUG):
        super().__init__(host, port, debug_mode)

        self.__wlan = wlan
        self.hostname = self.__wlan.ifconfig()[0]
        self.config = Config

    async def __requests_handler(self, client_r: StreamReader, client_w: StreamWriter):
        self.__print_debug(f"connection from: {client_w.get_extra_info('peername')}")

        try:
            request = await asyncio.wait_for(self.__load_request(client_r), self.config.TIMEOUT)

            if request:
                response = Response(301)
                response.add_header("LOCATION", f"https://{self.hostname}{request.url}")

                requests_utils.write_to_stream(client_w, response.get_response_string())
                await client_w.drain()

        except Exception as e:
            self.__print_debug(f"error occurred: {str(e)}", exception=e)

        finally:
            client_w.close()
            await client_w.wait_closed()

            self.__print_debug(f"connection closed")
