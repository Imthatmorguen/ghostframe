import os
import json

CONFIG_DIR = os.path.expanduser("~/.ghostframe")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "language": "en",
    "export_json": False,
    "export_html": False
}


# -------------------------
# LOAD CONFIG
# -------------------------

def load_config():
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    try:
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)

        # ensure missing keys won't break system
        for k, v in DEFAULT_CONFIG.items():
            if k not in data:
                data[k] = v

        return data

    except Exception:
        # auto-repair corrupted config
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG


# -------------------------
# SAVE CONFIG
# -------------------------

def save_config(cfg):
    os.makedirs(CONFIG_DIR, exist_ok=True)

    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)
