from lightberry.config.base_config import BaseConfig


class ServerConfig(BaseConfig):
    DEBUG: bool = False
    SERVER_PORT: int = 80
    WIFI_SSID: str = ""
    WIFI_PASSWORD: str = ""
    WIFI_AUTO_RECONNECT: bool = True
    HOTSPOT_MODE: bool = False
    HOTSPOT_NAME: str = ""
    HOTSPOT_PASSWORD: str = ""
    BLINK_LED: bool = True
    CERT_FILE: str = ""
    CERT_KEY: str = ""


ServerConfig.setup(section="Server")
