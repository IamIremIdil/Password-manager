import tkinter as tk
from tkinter import messagebox
from core import *  # Import all functions from core.py


class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager 🔐")

        if not os.path.exists("secret.key"):
            generate_key()
        self.key = load_key()
        self.passwords = load_passwords()

        # GUI setup (buttons, labels, etc.)
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Password Manager", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="➕ Add Password", command=self.add_password).pack(pady=5)
        tk.Button(self.root, text="👀 View Passwords", command=self.view_passwords).pack(pady=5)
        tk.Button(self.root, text="❌ Delete Password", command=self.delete_password).pack(pady=5)

    # Rest of your Tkinter methods (add_password, view_passwords, etc.)
    # ...


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()