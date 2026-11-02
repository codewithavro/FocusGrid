# views/dashboard_view.py
import os
import sys
import customtkinter as ctk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tasks_manager import TasksManager
from auth import AuthManager


class DashboardView(ctk.CTkFrame):

    def __init__(self, master, username, switch_to_login):
        super().__init__(master, fg_color="#181D28")

        self.username = username
        self.switch_to_login = switch_to_login

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Top Header Bar
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=20)
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.welcome_label = ctk.CTkLabel(
            self.header_frame,
            text=f"Welcome, {self.username} (FocusGrid Workspace)",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#00E5FF"
        )
        self.welcome_label.grid(row=0, column=0, sticky="w")

        # Action Buttons Frame on Header Right
        self.actions_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.actions_frame.grid(row=0, column=1, sticky="e")

        self.delete_btn = ctk.CTkButton(
            self.actions_frame,
            text="Delete Account",
            width=120,
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            command=self.prompt_delete_account
        )
        self.delete_btn.pack(side="left", padx=5)

        self.logout_btn = ctk.CTkButton(
            self.actions_frame,
            text="Logout",
            width=90,
            fg_color="#512DA8",
            hover_color="#FF5722",
            command=self.switch_to_login
        )
        self.logout_btn.pack(side="left", padx=5)

        # Main Content Card for Tasks
        self.card = ctk.CTkFrame(self, corner_radius=20, fg_color="#F8F9FD")
        self.card.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 30))
        self.card.grid_columnconfigure(0, weight=1)
        self.card.grid_rowconfigure(3, weight=1)

        self.title_label = ctk.CTkLabel(
            self.card,
            text="Your Personal Tasks",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#0D8A82"
        )
        self.title_label.grid(row=0, column=0, pady=(20, 10))

        # Task Input Section
        self.input_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, pady=10)

        self.task_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Enter a new task...",
            width=300,
            height=40,
            border_color="#00BCD4",
            border_width=2
        )
        self.task_entry.pack(side="left", padx=5)

        self.add_btn = ctk.CTkButton(
            self.input_frame,
            text="Add Task",
            width=100,
            height=40,
            fg_color="#512DA8",
            hover_color="#FF5722",
            command=self.handle_add_task
        )
        self.add_btn.pack(side="left", padx=5)

        # Feedback/Error Label (e.g. for account deletion errors)
        self.feedback_label = ctk.CTkLabel(
            self.card,
            text="",
            text_color="#E53935",
            font=ctk.CTkFont(size=12)
        )
        self.feedback_label.grid(row=2, column=0, pady=2)

        # Task Scrollable List Container
        self.tasks_scroll_frame = ctk.CTkScrollableFrame(
            self.card,
            fg_color="#FFFFFF",
            corner_radius=12,
            width=420,
            height=240
        )
        self.tasks_scroll_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.tasks_scroll_frame.grid_columnconfigure(0, weight=1)

        # Load existing tasks for this user
        self.refresh_task_list()

    def refresh_task_list(self):
        """Clears and re-renders the task list from local storage."""
        for widget in self.tasks_scroll_frame.winfo_children():
            widget.destroy()

        tasks = TasksManager.get_user_tasks(self.username)

        if not tasks:
            empty_label = ctk.CTkLabel(
                self.tasks_scroll_frame,
                text="No tasks added yet. Create one above!",
                text_color="#7A869A"
            )
            empty_label.pack(pady=20)
            return

        for index, item in enumerate(tasks):
            row_frame = ctk.CTkFrame(self.tasks_scroll_frame, fg_color="#F1F3F9", corner_radius=8)
            row_frame.pack(fill="x", pady=4, padx=5)
            row_frame.grid_columnconfigure(0, weight=1)

            t_label = ctk.CTkLabel(
                row_frame,
                text=item["task"],
                text_color="#181D28",
                anchor="w"
            )
            t_label.grid(row=0, column=0, padx=10, pady=8, sticky="w")

            del_btn = ctk.CTkButton(
                row_frame,
                text="Delete",
                width=60,
                height=28,
                fg_color="#E53935",
                hover_color="#C62828",
                command=lambda idx=index: self.handle_delete_task(idx)
            )
            del_btn.grid(row=0, column=1, padx=8, pady=8)

    def handle_add_task(self):
        """Adds a task and updates the UI."""
        task_text = self.task_entry.get()
        success, _ = TasksManager.add_task(self.username, task_text)
        if success:
            self.task_entry.delete(0, "end")
            self.refresh_task_list()

    def handle_delete_task(self, index):
        """Deletes a task and refreshes UI."""
        TasksManager.remove_task(self.username, index)
        self.refresh_task_list()

    def prompt_delete_account(self):
        """Prompts the user for confirmation and deletes their account permanently."""
        dialog = ctk.CTkInputDialog(
            text=f"Enter your password to permanently delete '{self.username}':",
            title="Confirm Account Deletion"
        )
        password = dialog.get_input()

        if password:
            success, message = AuthManager.delete_account(self.username, password)
            if success:
                self.switch_to_login()
            else:
                self.feedback_label.configure(text=message)