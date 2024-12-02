import json
import os

def load_config_into_env(config_file_path: str) -> None:
    with open(config_file_path) as config_file:
        config: dict = json.load(config_file)
    for key, value in config.items():
        if value is None:
            continue
        os.environ[key] = str(value)