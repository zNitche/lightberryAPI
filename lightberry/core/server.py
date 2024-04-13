import network
import time
import uasyncio
from lightberry.communication.request import Request
from lightberry.consts import HTTPConsts
from lightberry.utils import common_utils
from lightberry.config import Config


class Server:
    def __init__(self,
                 host="0.0.0.0",
                 port=Config.SERVER_PORT,
                 debug_mode=Config.DEBUG,
                 wifi_ssid=Config.WIFI_SSID,
                 wifi_password=Config.WIFI_PASSWORD,
                 wifi_connections_retries=5,
                 wifi_connection_retries_till_connected=False,
                 wifi_connection_delay=5,
                 hotspot_name=Config.HOTSPOT_NAME,
                 hotspot_password=Config.HOTSPOT_PASSWORD,
                 hotspot_mode=Config.HOTSPOT_MODE,
                 reconnect_to_network=Config.WIFI_AUTO_RECONNECT):

        self.host = host
        self.port = port

        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password

        self.wifi_connections_retries = wifi_connections_retries
        self.wifi_connection_retries_till_connected = wifi_connection_retries_till_connected
        self.wifi_connection_delay = wifi_connection_delay

        self.hotspot_name = hotspot_name
        self.hotspot_password = hotspot_password
        self.hotspot_mode = hotspot_mode

        self.wlan = None

        self.debug_mode = debug_mode
        self.reconnect_to_network = reconnect_to_network

        self.mainloop = uasyncio.get_event_loop()

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

        self.wlan.disconnect()

        while ((tries < self.wifi_connections_retries) or self.wifi_connection_retries_till_connected)\
                and (not self.wlan.isconnected()):

            self.__print_debug(f"connecting to network '{self.wifi_ssid}': {tries + 1}...")

            self.wlan.connect(self.wifi_ssid, self.wifi_password)

            time.sleep(self.wifi_connection_delay)
            tries += 1

        if self.wlan.isconnected():
            self.__print_debug(f"connected to '{self.wifi_ssid}'")
            self.__print_debug(f"WLAN config: {self.wlan.ifconfig()}")
        else:
            self.__print_debug(f"Couldn't connect to '{self.wifi_ssid}'")

    def __reconnect_to_network(self):
        if not self.wlan.isconnected() and not self.hotspot_mode:
            self.__print_debug(f"reconnecting to '{self.wifi_ssid}'")

            self.__connect_to_network()

    def init(self):
        self.__run_as_host() if self.hotspot_mode else self.__run_as_client()

    def __run_as_client(self):
        self.__setup_wlan_as_client()
        self.__connect_to_network()

    def __run_as_host(self):
        self.__setup_wlan_as_host()

    async def __load_request(self, request_stream):
        request_header_string = ""

        while True:
            request_line = await request_stream.readline()
            request_line = request_line.decode()

            # header end
            if request_line == "\r\n":
                break

            request_header_string += request_line

        self.__print_debug(f"request header string: {request_header_string}")

        request = Request()
        request.parse_header(request_header_string)

        content_length = request.header.get(HTTPConsts.CONTENT_LENGTH)

        if content_length:
            request_body_string = await request_stream.readexactly(int(content_length))
            request.parse_body(request_body_string.decode())

        self.__print_debug(f"request body string: {request.body}")

        return request

    async def __requests_handler(self, client_r, client_w):
        try:
            start_time = time.ticks_ms() if self.debug_mode else None

            client_address = client_w.get_extra_info("peername")

            request = await self.__load_request(client_r)
            self.__print_debug(f"connection from: {client_address}")

        except Exception as e:
            self.__print_debug(f"error occurred: {str(e)}", exception=e)

        finally:
            client_w.close()

            await client_w.wait_closed()

            self.__print_debug(f"request took: {time.ticks_ms() - start_time}ms")

    def start(self):
        self.__print_debug("starting mainloop...")

        if self.wlan is not None:
            self.mainloop.create_task(uasyncio.start_server(self.__requests_handler, self.host, self.port))

            if self.reconnect_to_network:
                self.__print_debug("wifi auto reconnect enabled...")

            self.__print_debug("mainloop running...")
            self.mainloop.run_forever()

    def stop(self):
        self.mainloop.stop()
        self.mainloop.close()

    def __print_debug(self, message, exception=None):
        common_utils.print_debug("SERVER", message, debug_enabled=self.debug_mode, exception=exception)
