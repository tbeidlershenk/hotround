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
        
def build_kaggle_config() -> None:
    kaggle_dir = os.path.expanduser("~/.kaggle")
    os.makedirs(kaggle_dir, exist_ok=True)
    kaggle_json_path = os.path.join(kaggle_dir, "kaggle.json")
    with open(kaggle_json_path, "w") as f:
        json.dump({
            "username": os.getenv("kaggle_username"),
            "key": os.getenv("kaggle_key")
        }, f, indent=4)
    os.chmod(kaggle_json_path, 0o600)
    
        