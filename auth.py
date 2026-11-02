import hashlib
import json
import os

# Path to store user credentials locally inside the data folder
USERS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "users.json"
)


class AuthManager:

  @staticmethod
  def _hash_password(password):
    """Hashes a password using SHA-256 for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

  @staticmethod
  def _load_users():
    """All registered users from the local JSON file."""
    if os.path.exists(USERS_PATH):
      try:
        with open(USERS_PATH, "r") as f:
          return json.load(f)
      except json.JSONDecodeError:
        return {}
    return {}

  @staticmethod
  def _save_users(users_dict):
    """Saves the users dictionary to the local JSON file."""
    os.makedirs(os.path.dirname(USERS_PATH), exist_ok=True)
    with open(USERS_PATH, "w") as f:
      json.dump(users_dict, f, indent=4)

  @staticmethod
  def signup(username, password, recovery_question, recovery_answer):
    """Registers a new user if the username is available."""
    users = AuthManager._load_users()

    if not username or not password:
      return False, "Username and password cannot be empty."

    if username in users:
      return False, "Username already exists. Choose another."

    users[username] = {
        "password": AuthManager._hash_password(password),
        "recovery_question": recovery_question,
        "recovery_answer": AuthManager._hash_password(recovery_answer),
    }

    AuthManager._save_users(users)
    return True, "Account created successfully!"

  @staticmethod
  def login(username, password):
    """Authenticates a user based on username and password."""
    users = AuthManager._load_users()

    if username not in users:
      return False, "Username not found."

    hashed_pw = AuthManager._hash_password(password)
    if users[username]["password"] == hashed_pw:
      return True, "Login successful!"

    return False, "Incorrect password."

  @staticmethod
  def get_recovery_question(username):
    """Retrieves the recovery question for a given username."""
    users = AuthManager._load_users()
    if username in users:
      return True, users[username].get(
          "recovery_question", "No question set."
      )
    return False, "Username not found."

  @staticmethod
  def reset_password(username, recovery_answer, new_password):
    """Resets the password if the recovery answer matches."""
    users = AuthManager._load_users()

    if username not in users:
      return False, "Username not found."

    hashed_answer = AuthManager._hash_password(recovery_answer)
    if users[username]["recovery_answer"] == hashed_answer:
      users[username]["password"] = AuthManager._hash_password(new_password)
      AuthManager._save_users(users)
      return True, "Password reset successfully!"

    return False, "Incorrect recovery answer."

  @staticmethod
  def signout(current_user_session):
    """Clears the active session state for signout."""
    return True, "Signed out successfully."

  @staticmethod
  def delete_account(username, password):
    """Deletes a user account and their stored tasks permanently after password verification."""
    users = AuthManager._load_users()

    if username not in users:
      return False, "User not found."

    # Hash the entered password to match how it's stored in users.json
    hashed_pw = AuthManager._hash_password(password)
    
    if users[username]["password"] == hashed_pw:
      # Remove user from users dictionary
      del users[username]
      AuthManager._save_users(users)
      
      # Clean up their stored tasks from tasks.json
      tasks_path = os.path.join(
          os.path.dirname(os.path.abspath(__file__)), "data", "tasks.json"
      )
      if os.path.exists(tasks_path):
        try:
          with open(tasks_path, "r") as f:
            tasks_data = json.load(f)
          if username in tasks_data:
            del tasks_data[username]
            with open(tasks_path, "w") as f:
              json.dump(tasks_data, f, indent=4)
        except Exception as e:
          print(f"Error clearing user tasks: {e}")
              
      return True, "Account deleted successfully."

    return False, "Incorrect password."