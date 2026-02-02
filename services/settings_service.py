import json
from pathlib import Path
from typing import Dict, Any

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "default_grade": "JG6",
    "auto_open_export": False,
    "developer_mode": False,
    "theme": "clam" 
}

class SettingsService:
    def __init__(self):
        self.settings_path = Path(SETTINGS_FILE)
        self.settings = self.load_settings()

    def load_settings(self) -> Dict[str, Any]:
        if not self.settings_path.exists():
            return DEFAULT_SETTINGS.copy()
        
        try:
            with open(self.settings_path, "r") as f:
                data = json.load(f)
                # Merge with defaults to ensure new keys exist
                return {**DEFAULT_SETTINGS, **data}
        except:
            return DEFAULT_SETTINGS.copy()

    def save_settings(self):
        try:
            with open(self.settings_path, "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def get(self, key: str):
        return self.settings.get(key, DEFAULT_SETTINGS.get(key))

    def set(self, key: str, value: Any):
        self.settings[key] = value
        self.save_settings()
