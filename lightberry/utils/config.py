from lightberry.utils.files import file_exists
import json


def load_config(file_path):
    config = {}

    if file_exists(file_path):
        with open(file_path, "r") as file:
            config = json.loads(file.read())

    return config


def from_config(key, config, fallback):
    val = config.get(key)

    return val if val else fallback
