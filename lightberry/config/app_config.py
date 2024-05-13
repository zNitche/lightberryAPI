from lightberry.config.base_config import BaseConfig


class AppConfig(BaseConfig):
    DEBUG: bool = False
    TIMEOUT: int = 10


AppConfig.setup(section="App", extend=True)
