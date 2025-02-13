from lightberry.config import ServerConfig as Config
from lightberry.core.sockets_servers.http import HttpSocketServer
from lightberry.utils import files_utils, requests_utils
import ssl
import asyncio

from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncio import StreamReader, StreamWriter
    from lightberry.core.app import App


class AppServer(HttpSocketServer):
    def __init__(self, app, host="0.0.0.0", port=Config.SERVER_PORT, debug_mode=Config.DEBUG):
        super().__init__(host, port, debug_mode)

        self.ssl_context: ssl.SSLContext | None = None

        self.__app: App = app
        self.config = Config

    async def __requests_handler(self, client_r: StreamReader, client_w: StreamWriter):
        try:
            request = await asyncio.wait_for(self.__load_request(client_r), self.config.TIMEOUT)

            if request:
                response = await asyncio.wait_for(self.__app.requests_handler(request), self.__app.config.TIMEOUT)

                if response.is_payload_streamed:
                    requests_utils.write_to_stream(client_w, response.get_headers_string())
                    await client_w.drain()

                    for chunk in response.get_body():
                        requests_utils.write_to_stream(client_w, chunk)
                        await client_w.drain()
                else:
                    requests_utils.write_to_stream(client_w, response.get_response_string())
                    await client_w.drain()

        except Exception as e:
            self.__print_debug(f"error occurred: {str(e)}", exception=e)

        finally:
            client_w.close()
            await client_w.wait_closed()

    def setup(self):
        ssl_cert_file = self.config.get("CERT_FILE")
        ssl_key_file = self.config.get("CERT_KEY")

        if files_utils.file_exists(ssl_cert_file) and files_utils.file_exists(ssl_key_file):
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.ssl_context.load_cert_chain(ssl_cert_file, ssl_key_file)

            self.port = 443

            self.__print_debug("SSL certificate has been loaded...")

        handler = self.__get_requests_handler_for_mode()
        self.server_task = asyncio.start_server(handler, self.host, self.port, ssl=self.ssl_context)
