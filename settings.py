import os
import json

def load_settings(json_path="settings.json"):
    global settings_group
    if not os.path.exists(json_path):
        print(f"Settings file '{json_path}' not found.")
        return {}
    with open(json_path, "r", encoding="utf-8") as f:
        try:
            settings_group = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}
    return settings_group