import os
import sys
import customtkinter as ctk
from PIL import Image

# Add parent directory to path for root-level module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import AuthManager


class SignupView(ctk.CTkFrame):

    def __init__(self, master, switch_to_login):
        # Dark outer frame background matching the app theme
        super().__init__(master, fg_color="#181D28")

        self.switch_to_login = switch_to_login

        # Configure grid weight for perfect centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Centered Off-White Card Container
        self.card = ctk.CTkFrame(
            self,
            corner_radius=24,
            fg_color="#F8F9FD",
            width=420
        )
        self.card.grid(row=0, column=0, padx=30, pady=20)
        self.card.grid_columnconfigure(0, weight=1)

        # 1. Logo Image (Compact size)
        self.load_logo()

        # 2. Title Header
        self.title_label = ctk.CTkLabel(
            self.card,
            text="Create an Account",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color="#0D8A82"
        )
        self.title_label.pack(pady=(12, 12))

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
            width=330,
            height=44
        )
        self.username_entry.pack(pady=7)

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
            width=330,
            height=44
        )
        self.password_entry.pack(pady=7)

        # 5. Recovery Question Entry
        self.recovery_q_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="Recovery Question (e.g., Pet's name)",
            placeholder_text_color="#7A869A",
            text_color="#181D28",
            font=ctk.CTkFont(size=14),
            fg_color="#FFFFFF",
            border_color="#00BCD4",
            border_width=2,
            corner_radius=12,
            width=330,
            height=44
        )
        self.recovery_q_entry.pack(pady=7)

        # 6. Recovery Answer Entry
        self.recovery_a_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="Recovery Answer",
            placeholder_text_color="#7A869A",
            text_color="#181D28",
            font=ctk.CTkFont(size=14),
            fg_color="#FFFFFF",
            border_color="#E91E63",
            border_width=2,
            corner_radius=12,
            width=330,
            height=44
        )
        self.recovery_a_entry.pack(pady=7)

        # Feedback/Error Label
        self.feedback_label = ctk.CTkLabel(
            self.card,
            text="",
            text_color="#E53935",
            font=ctk.CTkFont(size=12)
        )
        self.feedback_label.pack(pady=2)

        # 7. Sign Up Button
        self.signup_button = ctk.CTkButton(
            self.card,
            text="SIGN UP",
            font=ctk.CTkFont(family="Arial", size=15, weight="bold"),
            text_color="#FFFFFF",
            fg_color="#512DA8",
            hover_color="#FF5722",
            corner_radius=12,
            border_color="#00E5FF",
            border_width=1,
            width=330,
            height=44,
            command=self.handle_signup
        )
        self.signup_button.pack(pady=10)

        # 8. Back to Login Button
        self.back_button = ctk.CTkButton(
            self.card,
            text="Back to Login",
            font=ctk.CTkFont(size=14),
            text_color="#181D28",
            fg_color="#FFFFFF",
            border_color="#7A869A",
            border_width=1.5,
            corner_radius=12,
            width=330,
            height=40,
            command=self.switch_to_login
        )
        self.back_button.pack(pady=(5, 20))

    def load_logo(self):
        """Loads and displays the application logo inside the card."""
        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png"
        )

        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                self.logo_image = ctk.CTkImage(light_image=img, dark_image=img, size=(75, 75))
                self.logo_label = ctk.CTkLabel(self.card, image=self.logo_image, text="")
                self.logo_label.pack(pady=(15, 0))
            except Exception as e:
                print(f"Error loading logo: {e}")

    def handle_signup(self):
        """Processes account registration through AuthManager."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        question = self.recovery_q_entry.get().strip()
        answer = self.recovery_a_entry.get().strip()

        success, message = AuthManager.signup(username, password, question, answer)
        if success:
            self.feedback_label.configure(text_color="#2E7D32", text=message)
            self.after(1000, self.switch_to_login)
        else:
            self.feedback_label.configure(text_color="#D32F2F", text=message)