# tasks_manager.py
import json
import os

TASKS_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "tasks.json"
)

class TasksManager:

    @staticmethod
    def _load_tasks():
        """Loads all tasks from storage."""
        if os.path.exists(TASKS_FILE_PATH):
            try:
                with open(TASKS_FILE_PATH, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    @staticmethod
    def _save_tasks(tasks_data):
        """Saves tasks data to storage."""
        os.makedirs(os.path.dirname(TASKS_FILE_PATH), exist_ok=True)
        with open(TASKS_FILE_PATH, "w") as f:
            json.dump(tasks_data, f, indent=4)

    @classmethod
    def get_user_tasks(cls, username):
        """Retrieves task list for a specific user."""
        all_tasks = cls._load_tasks()
        return all_tasks.get(username, [])

    @classmethod
    def add_task(cls, username, task_text):
        """Adds a new task for a user and saves permanently."""
        if not task_text.strip():
            return False, "Task cannot be empty."
        
        all_tasks = cls._load_tasks()
        if username not in all_tasks:
            all_tasks[username] = []
            
        task_item = {"task": task_text.strip(), "completed": False}
        all_tasks[username].append(task_item)
        cls._save_tasks(all_tasks)
        return True, "Task added successfully!"

    @classmethod
    def remove_task(cls, username, index):
        """Removes a task by its index."""
        all_tasks = cls._load_tasks()
        if username in all_tasks and 0 <= index < len(all_tasks[username]):
            all_tasks[username].pop(index)
            cls._save_tasks(all_tasks)
            return True
        return False