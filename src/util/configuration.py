import json
import os

def load_config_into_env(config_file_path: str) -> None:
    with open(config_file_path) as config_file:
        config: dict = json.load(config_file)
    for key, value in config.items():
        if value is None:
            continue
        os.environ[key] = str(value)

def load_config_into_env_from_dict(config: dict) -> None:
    for key, value in config.items():
        if value is None:
            continue
        os.environ[key] = str(value)

def verify_config(vars: list[str]) -> None:
    for var in vars:
        if var in os.environ:
            continue
        else:
            raise ValueError(f"Missing environment variable: {var}")
        