from lightberry.config.base_config import BaseConfig


class ServerConfig(BaseConfig):
    DEBUG = False
    SERVER_PORT = 80
    WIFI_SSID = ""
    WIFI_PASSWORD = ""
    WIFI_AUTO_RECONNECT = True
    HOTSPOT_MODE = ""
    HOTSPOT_NAME = ""
    HOTSPOT_PASSWORD = ""
    BLINK_LED = True


ServerConfig.setup(section="Server")
