# theme.py
import customtkinter as ctk
import json
import os

THEME_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "theme_config.json"
)

# COLOR PALETTE (Vibrant Theme - based on generated design)
class Colors:
    CYAN = "#00FFFF"
    MAGENTA = "#FF00FF"
    GOLD = "#FFD700"
    DEEP_BLUE = "#1A1A2E" # Good background for dark mode
    BUTTON_LOGIN = "#00E5FF" # Vibrant Cyan for main button
    BUTTON_LOGIN_HOVER = "#00B8D4"
    TEXT_MAIN = "#FFFFFF"
    TEXT_SUB = "#AAAAAA"
    # To simulate gradients, we use contrasting fg_color and hover_color

class ThemeManager:

    @staticmethod
    def _load_config():
        """Loads theme preference (Light/Dark)."""
        if os.path.exists(THEME_CONFIG_PATH):
            try:
                with open(THEME_CONFIG_PATH, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {"appearance_mode": "Dark"} # Default
        return {"appearance_mode": "Dark"}

    @staticmethod
    def _save_config(mode):
        """Saves theme preference."""
        os.makedirs(os.path.dirname(THEME_CONFIG_PATH), exist_ok=True)
        with open(THEME_CONFIG_PATH, "w") as f:
            json.dump({"appearance_mode": mode}, f)

    @staticmethod
    def apply_saved_theme():
        """Applies the stored appearance mode on startup."""
        config = ThemeManager._load_config()
        mode = config.get("appearance_mode", "Dark")
        ctk.set_appearance_mode(mode)
        # Default color theme (built-in, but our views will override)
        ctk.set_default_color_theme("blue")

    @staticmethod
    def toggle_theme(current_mode):
        """Toggles between Dark and Light mode and saves preference."""
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        ThemeManager._save_config(new_mode)
        return new_mode