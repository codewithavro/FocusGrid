# main.py
import os
import sys
import customtkinter as ctk

# Ensure views and root modules are accessible
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from theme import ThemeManager
from views.login_view import LoginView
from views.signup_view import SignupView
from views.recovery_view import RecoveryView
from views.dashboard_view import DashboardView  # Import our new dashboard view

class FocusGridApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Configure window properties
        self.title("FocusGrid")
        self.geometry("900x650")
        self.minsize(800, 600)

        # Apply saved appearance mode
        ThemeManager.apply_saved_theme()

        # Configure container grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Track current active view
        self.current_view = None

        # Start by showing the Login view
        self.show_login()

    def clear_current_view(self):
        """Destroys the current view if it exists to prepare for a new screen."""
        if self.current_view is not None:
            self.current_view.destroy()

    def show_login(self):
        """Switches to the Login screen."""
        self.clear_current_view()
        self.current_view = LoginView(
            master=self,
            switch_to_dashboard=self.show_dashboard,
            switch_to_signup=self.show_signup,
            switch_to_recovery=self.show_recovery
        )
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def show_signup(self):
        """Switches to the Sign Up screen."""
        self.clear_current_view()
        self.current_view = SignupView(
            master=self,
            switch_to_login=self.show_login
        )
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def show_recovery(self):
        """Switches to the Password Recovery screen."""
        self.clear_current_view()
        self.current_view = RecoveryView(
            master=self,
            switch_to_login=self.show_login
        )
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def show_dashboard(self, username):
        """Switches to the Task Dashboard screen upon successful login."""
        self.clear_current_view()
        self.current_view = DashboardView(
            master=self,
            username=username,
            switch_to_login=self.show_login
        )
        self.current_view.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = FocusGridApp()
    app.mainloop()