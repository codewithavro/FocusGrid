import os
import sys
import customtkinter as ctk
from PIL import Image

# Add parent directory to path for root-level module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import AuthManager


class LoginView(ctk.CTkFrame):

    def __init__(self, master, switch_to_dashboard, switch_to_signup, switch_to_recovery):
        # Dark outer frame background matching the app theme
        super().__init__(master, fg_color="#181D28")

        self.switch_to_dashboard = switch_to_dashboard
        self.switch_to_signup = switch_to_signup
        self.switch_to_recovery = switch_to_recovery

        # Configure grid weight for perfect centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Center Card Container (Auto-sizing to fit all elements completely)
        self.card = ctk.CTkFrame(
            self,
            corner_radius=24,
            fg_color="#F8F9FD",
            width=420
        )
        self.card.grid(row=0, column=0, padx=30, pady=20)
        self.card.grid_columnconfigure(0, weight=1)

        # 1. Logo Image
        self.load_logo()

        # 2. Title Header
        self.title_label = ctk.CTkLabel(
            self.card,
            text="Welcome to FocusGrid",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color="#0D8A82"
        )
        self.title_label.pack(pady=(15, 12))

        # 3. Username Entry
        self.username_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="Username",
            placeholder_text_color="#7A869A",
            text_color="#181D28",
            font=ctk.CTkFont(size=14),
            fg_color="#FFFFFF",
            border_color="#00BCD4",
            border_width=2,
            corner_radius=12,
            width=340,
            height=45
        )
        self.username_entry.pack(pady=8)

        # 4. Password Entry
        self.password_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="Password",
            placeholder_text_color="#7A869A",
            text_color="#181D28",
            font=ctk.CTkFont(size=14),
            show="*",
            fg_color="#FFFFFF",
            border_color="#E91E63",
            border_width=2,
            corner_radius=12,
            width=340,
            height=45
        )
        self.password_entry.pack(pady=8)

        # Feedback/Error Label
        self.feedback_label = ctk.CTkLabel(
            self.card,
            text="",
            text_color="#E53935",
            font=ctk.CTkFont(size=12)
        )
        self.feedback_label.pack(pady=2)

        # 5. Login Button
        self.login_button = ctk.CTkButton(
            self.card,
            text="LOGIN",
            font=ctk.CTkFont(family="Arial", size=15, weight="bold"),
            text_color="#FFFFFF",
            fg_color="#512DA8",
            hover_color="#FF5722",
            corner_radius=12,
            border_color="#00E5FF",
            border_width=1,
            width=340,
            height=45,
            command=self.handle_login
        )
        self.login_button.pack(pady=12)

        # 6. Secondary Navigation Links (Sign Up & Forgot Password)
        self.nav_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.nav_frame.pack(pady=(5, 25))

        self.signup_btn = ctk.CTkButton(
            self.nav_frame,
            text="Sign Up",
            text_color="#181D28",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#FFFFFF",
            border_color="#0288D1",
            border_width=1.5,
            corner_radius=10,
            width=160,
            height=38,
            command=self.switch_to_signup
        )
        self.signup_btn.pack(side="left", padx=6)

        self.recovery_btn = ctk.CTkButton(
            self.nav_frame,
            text="Forgot Password?",
            text_color="#181D28",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#FFFFFF",
            border_color="#F57C00",
            border_width=1.5,
            corner_radius=10,
            width=160,
            height=38,
            command=self.switch_to_recovery
        )
        self.recovery_btn.pack(side="right", padx=6)

    def load_logo(self):
        """Loads and renders the geometric logo centered inside the card."""
        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png"
        )

        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                self.logo_image = ctk.CTkImage(light_image=img, dark_image=img, size=(85, 85))
                self.logo_label = ctk.CTkLabel(self.card, image=self.logo_image, text="")
                self.logo_label.pack(pady=(20, 0))
            except Exception as e:
                print(f"Error loading logo: {e}")

    def handle_login(self):
        """Handles authentication via AuthManager."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        success, message = AuthManager.login(username, password)
        if success:
            self.feedback_label.configure(text_color="#2E7D32", text=message)
            self.after(500, lambda: self.switch_to_dashboard(username))
        else:
            self.feedback_label.configure(text_color="#D32F2F", text=message)