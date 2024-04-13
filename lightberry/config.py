from lightberry.utils import config_utils as config_utils

config_file = config_utils.load_config("/config.json")


class Config:
    DEBUG = config_utils.from_config("DEBUG", config_file, 0)
    SERVER_PORT = config_utils.from_config("SERVER_PORT", config_file, 80)
    WIFI_SSID = config_utils.from_config("WIFI_SSID", config_file, "")
    WIFI_PASSWORD = config_utils.from_config("WIFI_PASSWORD", config_file, "")
    WIFI_AUTO_RECONNECT = config_utils.from_config("WIFI_AUTO_RECONNECT", config_file, True)
    HOTSPOT_MODE = config_utils.from_config("HOTSPOT_MODE", config_file, "")
    HOTSPOT_NAME = config_utils.from_config("HOTSPOT_NAME", config_file, "")
    HOTSPOT_PASSWORD = config_utils.from_config("HOTSPOT_PASSWORD", config_file, "")
