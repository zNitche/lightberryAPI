from lightberry.utils import config as config_utils

config_file = config_utils.load_config("/config.json")


class Config:
    DEBUG = config_utils.from_config("DEBUG", config_file, 0)
    WIFI_SSID = config_utils.from_config("WIFI_SSID", config_file, "")
    WIFI_PASSWORD = config_utils.from_config("WIFI_PASSWORD", config_file, "")
    HOTSPOT_MODE = config_utils.from_config("HOTSPOT_MODE", config_file, "")
    HOTSPOT_NAME = config_utils.from_config("HOTSPOT_NAME", config_file, "")
    HOTSPOT_PASSWORD = config_utils.from_config("HOTSPOT_PASSWORD", config_file, "")
