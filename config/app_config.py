from lightberry.config.base_config import BaseConfig


class AppConfig(BaseConfig):
    DEBUG = False


AppConfig.setup(section="App", extend=True)
