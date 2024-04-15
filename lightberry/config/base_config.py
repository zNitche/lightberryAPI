from lightberry.utils import config_utils as config_utils


class BaseConfig:
    @classmethod
    def setup(cls, section, extend=False):
        config_content = config_utils.get_config_section("/config.json", section)
        base_keys = cls.__dict__.keys()

        for key in config_content:
            if key in base_keys or extend:
                setattr(cls, key, config_content[key])
