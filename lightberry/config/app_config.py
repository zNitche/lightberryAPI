from lightberry.config.base_config import BaseConfig


class AppConfig(BaseConfig):
    DEBUG = 0


AppConfig.setup(section="App", extend=True)
