import network
import time
import asyncio
from lightberry.communication.request import Request
from lightberry.consts import ServerConsts
from lightberry.utils import common_utils
from lightberry.config import Config
from lightberry.core import periodic_tasks


class Server:
    def __init__(self,
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

        self.host = host
        self.port = port

        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password

        self.wifi_connections_retries = wifi_connections_retries

        self.hotspot_name = hotspot_name
        self.hotspot_password = hotspot_password
        self.hotspot_mode = hotspot_mode

        self.wlan = None

        self.debug_mode = debug_mode
        self.reconnect_to_network = reconnect_to_network

        self.mainloop = asyncio.get_event_loop()

        self.__run_as_host() if self.hotspot_mode else self.__run_as_client()

    def __setup_wlan_as_client(self):
        self.__print_debug(f"setting up server as client...")

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def __setup_wlan_as_host(self):
        self.__print_debug(f"setting up server as host...")

        self.wlan = network.WLAN(network.AP_IF)
        self.wlan.config(essid=self.hotspot_name, password=self.hotspot_password)

        self.wlan.active(True)

        self.__print_debug(f"WLAN config: {self.wlan.ifconfig()}")

    def __connect_to_network(self):
        tries = 0

        if not self.wlan.isconnected():
            self.wlan.disconnect()

        while (tries < self.wifi_connections_retries) and (not self.wlan.isconnected()):
            self.__print_debug(f"connecting to network '{self.wifi_ssid}': {tries + 1}...")

            self.wlan.connect(self.wifi_ssid, self.wifi_password)
            tries += 1

        if self.wlan.isconnected():
            self.__print_debug(f"connected to '{self.wifi_ssid}'")
            self.__print_debug(f"WLAN config: {self.wlan.ifconfig()}")
        else:
            self.__print_debug(f"Couldn't connect to '{self.wifi_ssid}'")

    def __run_as_client(self):
        self.__setup_wlan_as_client()
        self.__connect_to_network()

    def __run_as_host(self):
        self.__setup_wlan_as_host()

    async def __load_request(self, request_stream):
        try:
            request_header_string = ""

            while True:
                request_line = await request_stream.readline()
                request_line = request_line.decode()

                if request_line == "\r\n" or not request_line:
                    break

                request_header_string += request_line

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

    async def __requests_handler(self, client_r, client_w):
        try:
            start_time = time.ticks_ms() if self.debug_mode else None
            self.__print_debug(f"connection from: {client_w.get_extra_info('peername')}")

            request = await self.__load_request(client_r)

            if request:
                pass

        except Exception as e:
            self.__print_debug(f"error occurred: {str(e)}", exception=e)

        finally:
            client_w.close()
            await client_w.wait_closed()

            self.__print_debug(f"request took: {time.ticks_ms() - start_time}ms")

    def start(self):
        self.__print_debug("starting mainloop...")

        if self.wlan is not None:
            self.mainloop.create_task(asyncio.start_server(self.__requests_handler, self.host, self.port))

            if self.reconnect_to_network and not self.hotspot_mode:
                self.mainloop.create_task(periodic_tasks.reconnect_to_network(self.wlan.isconnected(),
                                                                              self.__connect_to_network,
                                                                              ServerConsts.WIFI_RECONNECT_PERIOD))

                self.__print_debug("wifi auto reconnect enabled...")

            self.__print_debug("mainloop running...")
            self.mainloop.run_forever()

    def stop(self):
        self.mainloop.stop()
        self.mainloop.close()

    def __print_debug(self, message, exception=None):
        common_utils.print_debug(message, "SERVER", debug_enabled=self.debug_mode, exception=exception)
