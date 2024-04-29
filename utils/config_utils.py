from lightberry.utils.files_utils import file_exists
import json


def load_config(file_path: str) -> dict[str, ...]:
    config = {}

    if file_exists(file_path):
        with open(file_path, "r") as file:
            config = json.loads(file.read())

    return config


def get_config_section(file_path: str, section: str) -> dict | None:
    config = load_config(file_path)

    return config.get(section) if config else None
