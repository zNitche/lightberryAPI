import network
import asyncio
import time
from lightberry.tasks import ConnectToNetworkTask, BlinkLedTask
from lightberry.core.sockets_servers.http import AppServer
from lightberry.core.sockets_servers.http import SslProxyServer
from lightberry.utils import common_utils
from lightberry.config import ServerConfig as Config

from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lightberry.core.app import App
    from lightberry.tasks import ATaskBase
    from lightberry.tasks import TaskBase
    from lightberry.core.sockets_servers.http import HttpSocketServer


class Server:
    def __init__(self,
                 app: App,
                 debug_mode=Config.DEBUG,
                 wifi_ssid=Config.WIFI_SSID,
                 wifi_password=Config.WIFI_PASSWORD,
                 wifi_connections_retries=5,
                 wifi_connection_timeout=5,
                 hotspot_name=Config.HOTSPOT_NAME,
                 hotspot_password=Config.HOTSPOT_PASSWORD,
                 hotspot_mode=Config.HOTSPOT_MODE,
                 reconnect_to_network=Config.WIFI_AUTO_RECONNECT):

        self.debug_mode = debug_mode
        self.config = Config

        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password

        self.__wifi_connections_retries = wifi_connections_retries
        self.__wifi_connection_timeout = wifi_connection_timeout

        self.hotspot_name = hotspot_name
        self.hotspot_password = hotspot_password
        self.__hotspot_mode = hotspot_mode

        self.__wlan: network.WLAN | None = None
        self.__wlan_enabled: bool = False

        self.__reconnect_to_network = reconnect_to_network

        self.__mainloop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self.__app = app

        self.__http_socket_servers: list[HttpSocketServer] = []

        self.__async_background_tasks: list[ATaskBase] = []
        self.__background_tasks: list[TaskBase] = []

    def __setup_wlan(self):
        self.__run_as_host() if self.__hotspot_mode else self.__run_as_client()

        if self.__wlan is not None:
            self.__print_debug(f"WLAN config: {self.__wlan.ifconfig()}", enabled=True)
            self.__print_debug(f"MAC Address: {self.get_mac()}", enabled=True)

            self.__wlan_enabled = True

    def toggle_wlan(self, enabled: bool):
        if enabled != self.__wlan_enabled:
            self.__wlan.active(enabled)
            self.__wlan_enabled = enabled

    def __setup_wlan_as_client(self):
        self.__print_debug(f"setting up server as client...")

        self.__wlan = network.WLAN(network.STA_IF)
        self.__wlan.active(True)
        self.__wlan.disconnect()

    def __run_as_client(self):
        self.__setup_wlan_as_client()

    def __run_as_host(self):
        self.__print_debug(f"setting up server as host...")

        self.__wlan = network.WLAN(network.AP_IF)
        self.__wlan.config(essid=self.hotspot_name, password=self.hotspot_password)
        self.__wlan.active(True)

    # for ConnectToNetworkTask
    async def __connect_to_network(self):
        if self.__wlan and not self.__wlan.isconnected() and self.__wlan_enabled:
            self.__print_debug(f"connecting to network '{self.wifi_ssid}'")
            self.__wlan.connect(self.wifi_ssid, self.wifi_password)

            timeout_time = time.time() + self.__wifi_connection_timeout
            while not self.__wlan.isconnected() or time.time() > timeout_time:
                await asyncio.sleep(0.5)

            if self.__wlan.isconnected():
                self.__print_debug(f"connected to '{self.wifi_ssid}', WLAN config: {self.__wlan.ifconfig()}")
            else:
                self.__print_debug(f"couldn't connect to '{self.wifi_ssid}'")

    def is_wlan_active(self) -> bool:
        return self.__wlan and self.__wlan_enabled

    def get_mac(self) -> str | None:
        if self.__wlan is None:
            return None

        return common_utils.get_readable_mac_address(self.__wlan.config("mac"))

    def get_host(self) -> str | None:
        if self.__wlan is None:
            return None

        return f"{self.__wlan.ifconfig()[0]}:{self.config.SERVER_PORT}"

    def __init_http_socket_servers(self):
        app_server = AppServer(self.__app, port=self.config.SERVER_PORT)
        app_server.setup()

        self.__http_socket_servers.append(app_server)

        if app_server.ssl_context is not None:
            proxy_server = SslProxyServer(self.__wlan, port=self.config.SERVER_PORT)
            proxy_server.setup()

            self.__http_socket_servers.append(proxy_server)

        for server in self.__http_socket_servers:  # type: HttpSocketServer
            self.__mainloop.create_task(server.server_task)
            self.__print_debug(f"[SOCKET SERVER] Task for {server.__class__.__name__} has been created")

    def __register_async_background_tasks(self):
        if self.__mainloop:
            if not self.__hotspot_mode:
                reconnect_task = ConnectToNetworkTask(is_wlan_enabled=self.is_wlan_active,
                                                      is_connected=self.__wlan.isconnected,
                                                      connection_handler=self.__connect_to_network,
                                                      retires=self.__wifi_connections_retries,
                                                      reconnect=self.__reconnect_to_network,
                                                      logging=self.debug_mode)

                self.__async_background_tasks.append(reconnect_task)

            if self.config.BLINK_LED:
                self.__async_background_tasks.append(BlinkLedTask())

            for task in self.__async_background_tasks:  # type: ATaskBase
                self.__mainloop.create_task(task.handler())
                self.__print_debug(f"[TASKS] registering async task: {task.__class__.__name__}")

    def __setup_app_server_handlers(self):
        self.__app.server_handlers_manager.setup_handler("get_mac_address", self.get_mac)
        self.__app.server_handlers_manager.setup_handler("get_host", self.get_host)
        self.__app.server_handlers_manager.setup_handler("toggle_wlan", self.toggle_wlan)
        self.__app.server_handlers_manager.setup_handler("is_wlan_active", self.is_wlan_active)

    def __setup_app(self):
        self.__app.register_async_background_tasks(self.__mainloop)
        self.__app.register_background_tasks()

    def start(self):
        self.__setup_wlan()
        self.__print_debug("starting mainloop...")

        if self.__wlan is not None:
            self.__init_http_socket_servers()

            self.__setup_app_server_handlers()

            self.__register_async_background_tasks()
            self.__setup_app()

            self.__print_debug(f"server listening at: {self.__app.server_handlers_manager.get_host()}")
            self.__print_debug("mainloop running...")

            self.__mainloop.run_forever()

        else:
            self.__print_debug("Couldn't start server wlan is None")

    def stop(self):
        self.__mainloop.stop()
        self.__mainloop.close()

        self.toggle_wlan(enabled=False)

    def __print_debug(self, message: str, exception: Exception | None = None, enabled: bool | None = None):
        common_utils.print_debug(message, "SERVER",
                                 debug_enabled=enabled if enabled is not None else self.debug_mode,
                                 exception=exception)
