import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "app_name": "BLACKOUT",
    "version": "2.0.0",
    "author": "DAPZ",
    "theme": "cyan",
    "logging": True
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)
