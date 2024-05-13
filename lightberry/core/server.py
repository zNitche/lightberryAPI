import network
import ssl
import time
import asyncio
from lightberry.core.communication.request import Request
from lightberry.tasks.periodic_tasks import ReconnectToNetworkTask, BlinkLedTask
from lightberry.utils import common_utils, requests_utils, files_utils
from lightberry.config import ServerConfig as Config

from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from network import WLAN
    from asyncio import AbstractEventLoop, StreamReader, StreamWriter
    from lightberry.core.app import App
    from lightberry.tasks.task_base import TaskBase


class Server:
    def __init__(self,
                 app: App,
                 host="0.0.0.0",
                 port=Config.SERVER_PORT,
                 debug_mode=Config.DEBUG,
                 wifi_ssid=Config.WIFI_SSID,
                 wifi_password=Config.WIFI_PASSWORD,
                 wifi_connections_retries=5,
                 hotspot_name=Config.HOTSPOT_NAME,
                 hotspot_password=Config.HOTSPOT_PASSWORD,
                 hotspot_mode=Config.HOTSPOT_MODE,
                 reconnect_to_network=Config.WIFI_AUTO_RECONNECT):

        self.debug_mode = debug_mode
        self.config = Config

        self.host = host
        self.port = port

        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password

        self.__wifi_connections_retries = wifi_connections_retries

        self.hotspot_name = hotspot_name
        self.hotspot_password = hotspot_password
        self.__hotspot_mode = hotspot_mode

        self.__wlan: WLAN | None = None
        self.__reconnect_to_network = reconnect_to_network

        self.__mainloop: AbstractEventLoop = asyncio.get_event_loop()
        self.__app = app

        self.__background_tasks: list[TaskBase] = []

        self.__run_as_host() if self.__hotspot_mode else self.__run_as_client()

    def __setup_wlan_as_client(self):
        self.__print_debug(f"setting up server as client...")

        self.__wlan = network.WLAN(network.STA_IF)
        self.__wlan.active(True)

    def __setup_wlan_as_host(self):
        self.__print_debug(f"setting up server as host...")

        self.__wlan = network.WLAN(network.AP_IF)
        self.__wlan.config(essid=self.hotspot_name, password=self.hotspot_password)

        self.__wlan.active(True)
        self.__print_debug(f"WLAN config: {self.__wlan.ifconfig()}")

    def __connect_to_network(self):
        tries = 0

        if not self.__wlan.isconnected():
            self.__wlan.disconnect()

        while (tries < self.__wifi_connections_retries) and (not self.__wlan.isconnected()):
            self.__print_debug(f"connecting to network '{self.wifi_ssid}': {tries + 1}...")

            self.__wlan.connect(self.wifi_ssid, self.wifi_password)
            tries += 1

        if self.__wlan.isconnected():
            self.__print_debug(f"connected to '{self.wifi_ssid}'")
            self.__print_debug(f"WLAN config: {self.__wlan.ifconfig()}")
        else:
            self.__print_debug(f"Couldn't connect to '{self.wifi_ssid}'")

    def __run_as_client(self):
        self.__setup_wlan_as_client()
        self.__connect_to_network()

    def __run_as_host(self):
        self.__setup_wlan_as_host()

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
        self.__print_debug(f"connection from: {client_w.get_extra_info('peername')}")

        try:
            start_time = time.ticks_ms() if self.debug_mode else None

            request = await asyncio.wait_for(self.__load_request(client_r), self.config.TIMEOUT)

            if request:
                response = await asyncio.wait_for(self.__app.requests_handler(request), self.__app.config.TIMEOUT)

                if response.is_payload_streamed:
                    client_w.write(bytes(f"{response.get_headers()}\r\n\r\n", "utf-8"))
                    await client_w.drain()

                    for chunk in response.get_body():
                        client_w.write(bytes(chunk, "utf-8"))
                        await client_w.drain()
                else:
                    client_w.write(bytes(response.get_response_string(), "utf-8"))
                    await client_w.drain()

        except Exception as e:
            self.__print_debug(f"error occurred: {str(e)}", exception=e)

        finally:
            client_w.close()
            await client_w.wait_closed()

            if self.debug_mode:
                self.__print_debug(f"request took: {time.ticks_ms() - start_time}ms")

    def __init_server(self):
        ssl_context = None
        ssl_cert_file = self.config.get("CERT_FILE")
        ssl_key_file = self.config.get("CERT_KEY")

        if ((ssl_cert_file and files_utils.file_exists(ssl_cert_file)) and
                (ssl_key_file and files_utils.file_exists(ssl_key_file))):
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(ssl_cert_file, ssl_key_file)

            self.__print_debug("SSL certificate has been loaded...")

        target_port = self.port if ssl_context is None else 443
        server_task = asyncio.start_server(self.__requests_handler,
                                           self.host,
                                           target_port,
                                           ssl=ssl_context)

        self.__mainloop.create_task(server_task)

    def start(self):
        self.__print_debug("starting mainloop...")

        if self.__wlan is not None:
            self.__init_server()

            self.__register_background_tasks()
            self.__setup_app()

            self.__print_debug(f"server listening at: {self.__app.host}")
            self.__print_debug("mainloop running...")

            self.__mainloop.run_forever()

    def stop(self):
        self.__mainloop.stop()
        self.__mainloop.close()

    def __setup_app(self):
        self.__app.host = f"{self.__wlan.ifconfig()[0]}:{self.port}"
        self.__app.register_background_tasks(self.__mainloop)

    def __register_background_tasks(self):
        if self.__mainloop:
            if self.__reconnect_to_network and not self.__hotspot_mode:
                self.__background_tasks.append(ReconnectToNetworkTask(self.__wlan.isconnected,
                                                                      self.__connect_to_network,
                                                                      self.debug_mode))

            if self.config.BLINK_LED:
                self.__background_tasks.append(BlinkLedTask())

            for task in self.__background_tasks:
                self.__mainloop.create_task(task.handler())
                self.__print_debug(f"registering task: {task.__class__.__name__}")

    def __print_debug(self, message: str, exception: Exception | None = None):
        common_utils.print_debug(message, "SERVER", debug_enabled=self.debug_mode, exception=exception)
