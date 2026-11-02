import os
import sys
import customtkinter as ctk

# Add parent directory to path for root-level module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import AuthManager


class RecoveryView(ctk.CTkFrame):

  def __init__(self, master, switch_to_login):
    super().__init__(master)

    self.switch_to_login = switch_to_login

    # Configure grid weight for centering
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(0, weight=1)

    # Main container frame
    self.container = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
    self.container.grid(row=0, column=0, padx=20, pady=20)

    # Title Label
    self.title_label = ctk.CTkLabel(
        self.container, text="Reset Password", font=ctk.CTkFont(size=22, weight="bold")
    )
    self.title_label.pack(pady=(10, 20))

    # Username Entry
    self.username_entry = ctk.CTkEntry(
        self.container, placeholder_text="Enter Username", width=250, height=35
    )
    self.username_entry.pack(pady=10)

    # Fetch Question Button
    self.fetch_button = ctk.CTkButton(
        self.container, text="Get Security Question", width=250, height=30, command=self.fetch_question
    )
    self.fetch_button.pack(pady=5)

    # Security Question Display Label
    self.question_display = ctk.CTkLabel(
        self.container, text="Security Question: (Enter username first)", text_color="gray", font=ctk.CTkFont(size=12), wraplength=250
    )
    self.question_display.pack(pady=10)

    # Recovery Answer Entry
    self.answer_entry = ctk.CTkEntry(
        self.container, placeholder_text="Recovery Answer", show="*", width=250, height=35
    )
    self.answer_entry.pack(pady=10)

    # New Password Entry
    self.new_password_entry = ctk.CTkEntry(
        self.container, placeholder_text="New Password", show="*", width=250, height=35
    )
    self.new_password_entry.pack(pady=10)

    # Status/Feedback Label
    self.feedback_label = ctk.CTkLabel(self.container, text="", text_color="red", font=ctk.CTkFont(size=12))
    self.feedback_label.pack(pady=5)

    # Reset Password Button
    self.reset_button = ctk.CTkButton(
        self.container, text="Reset Password", width=250, height=35, command=self.handle_reset
    )
    self.reset_button.pack(pady=10)

    # Back to Login Button
    self.back_button = ctk.CTkButton(
        self.container, text="Back to Login", width=250, fg_color="transparent", border_width=1, command=self.switch_to_login
    )
    self.back_button.pack(pady=5)

  def fetch_question(self):
    """Fetches and displays the security question for the given username."""
    username = self.username_entry.get().strip()
    if not username:
      self.feedback_label.configure(text_color="red", text="Please enter a username.")
      return

    success, result = AuthManager.get_recovery_question(username)
    if success:
      self.question_display.configure(text=f"Question: {result}", text_color="cyan")
      self.feedback_label.configure(text="")
    else:
      self.question_display.configure(text="Security Question: (Not found)", text_color="gray")
      self.feedback_label.configure(text_color="red", text=result)

  def handle_reset(self):
    """Processes password reset through the AuthManager backend."""
    username = self.username_entry.get().strip()
    answer = self.answer_entry.get().strip()
    new_password = self.new_password_entry.get().strip()

    if not username or not answer or not new_password:
      self.feedback_label.configure(text_color="red", text="All fields are required.")
      return

    success, message = AuthManager.reset_password(username, answer, new_password)
    if success:
      self.feedback_label.configure(text_color="green", text=message)
      self.after(1000, self.switch_to_login)
    else:
      self.feedback_label.configure(text_color="red", text=message)