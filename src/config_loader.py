import os
import json
from typing import Dict, Any

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config')
CONFIG_FILE = os.path.join(CONFIG_PATH, 'global_config.json')

def load_config() -> Dict[str, Any]:
    if not os.path.exists(CONFIG_FILE):
        print("⚠️ No config file found.")
        return {}

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            print("⚙️ Config loaded successfully.")
            return config
    except (json.JSONDecodeError, FileNotFoundError):
        print("❌ Failed to parse config file.")
        return {}