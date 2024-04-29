from lightberry.utils import config_utils as config_utils


class BaseConfig:
    @classmethod
    def setup(cls, section: str, extend: bool = False):
        config_content = config_utils.get_config_section("/lightberry_config.json", section)

        if config_content:
            base_keys = cls.__dict__.keys()

            for key in config_content:
                if key in base_keys or extend:
                    setattr(cls, key, config_content[key])

    @classmethod
    def get(cls, key: str):
        return cls.__dict__.get(key)
