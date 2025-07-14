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
    ###1)

    def add_password(self):
        # Create pop-up window
        add_window = tk.Toplevel(self.root)
        add_window.title("➕ Add New Password")
        add_window.geometry("300x200")

        # Website
        tk.Label(add_window, text="Website:").pack(pady=5)
        website_entry = tk.Entry(add_window)
        website_entry.pack()

        # Username
        tk.Label(add_window, text="Username:").pack(pady=5)
        username_entry = tk.Entry(add_window)
        username_entry.pack()

        # Password
        tk.Label(add_window, text="Password:").pack(pady=5)
        password_entry = tk.Entry(add_window, show="•")
        password_entry.pack()

        # Save Button
        def save():
            website = website_entry.get()
            username = username_entry.get()
            password = password_entry.get()

            if not all([website, username, password]):
                messagebox.showerror("Error", "All fields are required!")
                return

            # Encrypt and save
            self.passwords[website] = {
                "username": username,
                "password": encrypt_password(password, self.key)
            }
            save_passwords(self.passwords)
            messagebox.showinfo("Success", "Password saved!")
            add_window.destroy()

        tk.Button(add_window, text="💾 Save", command=save).pack(pady=10)

    def view_passwords(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("🔍 Saved Passwords")
        view_window.geometry("500x300")

        if not self.passwords:
            tk.Label(view_window, text="No passwords stored yet!").pack()
            return

            # Create scrollable frame
        canvas = tk.Canvas(view_window)
        scrollbar = tk.Scrollbar(view_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

            # Display each password
        for website, data in self.passwords.items():
            frame = tk.Frame(scrollable_frame, relief=tk.RIDGE, bd=1)
            frame.pack(fill=tk.X, padx=5, pady=2)

            decrypted_pass = decrypt_password(data["password"], self.key)

            tk.Label(frame, text=f"🌐 {website}", width=20, anchor="w").pack(side="left")
            tk.Label(frame, text=f"👤 {data['username']}", width=25, anchor="w").pack(side="left")
            tk.Label(frame, text=f"🔑 {decrypted_pass}", width=25, anchor="w").pack(side="left")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def delete_password(self):
        if not self.passwords:
            messagebox.showinfo("Info", "No passwords to delete!")
            return

        del_window = tk.Toplevel(self.root)
        del_window.title("❌ Delete Password")

        # Website selection
        tk.Label(del_window, text="Select website to delete:").pack(pady=5)

        website_var = tk.StringVar(del_window)
        website_var.set(list(self.passwords.keys())[0])  # Default to first

        website_menu = tk.OptionMenu(del_window, website_var, *self.passwords.keys())
        website_menu.pack(pady=5)

            # Delete button
        def confirm_delete():
            website = website_var.get()
            del self.passwords[website]
            save_passwords(self.passwords)
            messagebox.showinfo("Deleted", f"Removed credentials for {website}")
            del_window.destroy()

        tk.Button(
            del_window,
            text="⚠️ Delete",
            command=confirm_delete,
            fg="red"
        ).pack(pady=10)

    # Rest of your Tkinter methods (add_password, view_passwords, etc.)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()