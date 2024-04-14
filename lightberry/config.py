from lightberry.utils import config_utils as config_utils


class Config:
    DEBUG = 0
    SERVER_PORT = 80
    WIFI_SSID = ""
    WIFI_PASSWORD = ""
    WIFI_AUTO_RECONNECT = True
    HOTSPOT_MODE = ""
    HOTSPOT_NAME = ""
    HOTSPOT_PASSWORD = ""

    @classmethod
    def setup(cls):
        config_file = config_utils.load_config("/config.json")
        base_keys = cls.__dict__.keys()

        for key in config_file:
            if key in base_keys:
                setattr(cls, key, config_file[key])


Config.setup()
