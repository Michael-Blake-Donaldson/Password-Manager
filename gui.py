import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from database import Database
from encryption import Encryption
import re

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # Hide the root window initially
        self.db = Database()

        self.root.iconbitmap('C:/Users/blake/OneDrive/Desktop/VS Projects/PasswordManager/icons8-test-account-16.png')  # Add your icon here

        master_password_data = self.db.get_master_password()
        
        if master_password_data:
            self.encryption = Encryption(master_password_data['key'].encode())
            self.master_password = master_password_data['master_password']
            self.master_password_prompt()
        else:
            self.encryption = Encryption()  # Generate a new key
            self.set_master_password_prompt()

    def apply_custom_theme(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')

        # Custom styles
        style.configure('TButton', font=('Helvetica', 10), padding=8, relief='flat', background='#3498db', foreground='white')
        style.map('TButton', background=[('active', '#2980b9')], foreground=[('active', 'white')])
        style.configure('TLabel', font=('Helvetica', 10), background='#ecf0f1')
        style.configure('TEntry', font=('Helvetica', 10), padding=5)
        style.configure('TFrame', background='#ecf0f1')

        # Root window background
        self.root.configure(background='#ecf0f1')

    def setup_main_gui(self):
        self.apply_custom_theme()
        self.root.title("Password Manager")
        self.root.geometry("450x400")

        # Header Frame
        header_frame = ttk.Frame(self.root, relief='ridge', padding=10)
        header_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 20))

        # Add a title to the header
        title_label = ttk.Label(header_frame, text="Password Manager", font=('Helvetica', 16, 'bold'), anchor='center')
        title_label.pack()

        # Content Frame for entries and buttons
        content_frame = ttk.Frame(self.root, padding=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Entry Fields in the content frame using grid for alignment
        self.website_label = ttk.Label(content_frame, text="Website:")
        self.website_label.grid(row=0, column=0, padx=5, pady=10, sticky=tk.E)

        self.website_entry = ttk.Entry(content_frame, width=30)
        self.website_entry.grid(row=0, column=1, padx=5, pady=10)

        self.password_label = ttk.Label(content_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=10, sticky=tk.E)

        self.password_entry = ttk.Entry(content_frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=5, pady=10)

        # Buttons in the content frame
        self.add_button = ttk.Button(content_frame, text="Add Password", command=self.add_password, style='TButton')
        self.add_button.grid(row=2, column=0, padx=5, pady=10, sticky=tk.W)

        self.view_button = ttk.Button(content_frame, text="View Passwords", command=self.view_passwords, style='TButton')
        self.view_button.grid(row=2, column=1, padx=5, pady=10, sticky=tk.E)

        self.search_button = ttk.Button(content_frame, text="Search Password", command=self.search_password, style='TButton')
        self.search_button.grid(row=3, column=0, padx=5, pady=10, sticky=tk.W)

        self.update_button = ttk.Button(content_frame, text="Update Password", command=self.update_password, style='TButton')
        self.update_button.grid(row=3, column=1, padx=5, pady=10, sticky=tk.E)

        self.delete_button = ttk.Button(content_frame, text="Delete Password", command=self.delete_password, style='TButton')
        self.delete_button.grid(row=4, column=0, padx=5, pady=10, sticky=tk.W)

        self.export_button = ttk.Button(content_frame, text="Export Passwords", command=self.export_passwords, style='TButton')
        self.export_button.grid(row=4, column=1, padx=5, pady=10, sticky=tk.E)

        # Bottom Status Bar
        self.status = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, message):
        self.status.config(text=message)

    def is_strong_password(self, password):
        if len(password) < 8:
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    def set_master_password_prompt(self):
        self.master_window = tk.Toplevel(self.root)
        self.master_window.title("Set Master Password")
        self.master_window.geometry("300x150")
        self.master_window.configure(background='#ecf0f1')

        ttk.Label(self.master_window, text="Set Master Password:", background='#ecf0f1').pack(pady=(20, 10))
        self.master_password_entry = ttk.Entry(self.master_window, show="*", width=25)
        self.master_password_entry.pack(pady=(0, 10))

        ttk.Button(self.master_window, text="Submit", command=self.set_master_password, style='TButton').pack(pady=(10, 20))

    def set_master_password(self):
        password = self.master_password_entry.get()
        if password:
            if self.is_strong_password(password):
                encrypted_password = self.encryption.encrypt(password)
                self.db.store_master_password(encrypted_password, self.encryption.get_key())
                messagebox.showinfo("Success", "Master Password Set Successfully!")
                self.master_window.destroy()
                self.root.deiconify()  # Show the main window
                self.setup_main_gui()
            else:
                messagebox.showerror("Error", "Password is not strong enough!")
        else:
            messagebox.showwarning("Input Error", "Please enter a password.")

    def master_password_prompt(self):
        self.master_window = tk.Toplevel(self.root)
        self.master_window.title("Master Password")
        self.master_window.geometry("300x150")
        self.master_window.configure(background='#ecf0f1')

        ttk.Label(self.master_window, text="Enter Master Password:", background='#ecf0f1').pack(pady=(20, 10))
        self.master_password_entry = ttk.Entry(self.master_window, show="*", width=25)
        self.master_password_entry.pack(pady=(0, 10))

        ttk.Button(self.master_window, text="Submit", command=self.check_master_password, style='TButton').pack(pady=(10, 5))
        ttk.Button(self.master_window, text="Forgot Password?", command=self.reset_master_password, style='TButton').pack(pady=(5, 20))

    def check_master_password(self):
        entered_password = self.master_password_entry.get()
        try:
            decrypted_password = self.encryption.decrypt(self.master_password)
            if decrypted_password == entered_password:
                messagebox.showinfo("Success", "Access Granted!")
                self.master_window.destroy()
                self.root.deiconify()  # Show the main window
                self.setup_main_gui()
            else:
                messagebox.showerror("Error", "Access Denied!")
        except Exception as e:
            print(f"Decryption failed: {e}")
            messagebox.showerror("Error", "Invalid Master Password!")

    def reset_master_password(self):
        reset_window = tk.Toplevel(self.root)
        reset_window.title("Reset Master Password")
        reset_window.geometry("300x150")
        reset_window.configure(background='#ecf0f1')

        ttk.Label(reset_window, text="Enter Reset Code:", background='#ecf0f1').pack(pady=(20, 10))
        reset_code_entry = ttk.Entry(reset_window, width=25)
        reset_code_entry.pack(pady=(0, 10))

        def perform_reset():
            reset_code = reset_code_entry.get()
            if reset_code == "your_reset_code":  # Replace with your desired reset code
                self.set_master_password_prompt()
                reset_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid Reset Code!")

        ttk.Button(reset_window, text="Submit", command=perform_reset, style='TButton').pack(pady=(10, 20))

    def add_password(self):
        website = self.website_entry.get()
        password = self.password_entry.get()

        if website and password:
            encrypted_password = self.encryption.encrypt(password)
            self.db.insert_password({"website": website, "password": encrypted_password})
            self.update_status("Password added successfully!")
            self.website_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            self.update_status("Please fill out all fields.")

    def view_passwords(self):
        passwords = self.db.get_all_passwords()

        # Create a new window to display passwords
        view_window = tk.Toplevel(self.root)
        view_window.title("Stored Passwords")
        view_window.geometry("400x300")
        view_window.configure(background='#ecf0f1')

        # Display the passwords
        for idx, pwd in enumerate(passwords):
            decrypted_password = self.encryption.decrypt(pwd['password'])
            password_label = ttk.Label(view_window, text=f"Website: {pwd['website']} | Password: {decrypted_password}", background='#ecf0f1')
            password_label.pack(pady=5)

    def search_password(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Password")
        search_window.geometry("300x150")
        search_window.configure(background='#ecf0f1')

        search_label = ttk.Label(search_window, text="Enter Website:", background='#ecf0f1')
        search_label.pack(pady=(20, 10))

        search_entry = ttk.Entry(search_window, width=25)
        search_entry.pack(pady=(0, 10))

        def perform_search():
            website = search_entry.get()
            result = self.db.find_password({"website": website})
            if result:
                decrypted_password = self.encryption.decrypt(result['password'])
                result_label = ttk.Label(search_window, text=f"Password for {website}: {decrypted_password}", background='#ecf0f1')
                result_label.pack(pady=5)
            else:
                result_label = ttk.Label(search_window, text="Website not found.", background='#ecf0f1')
                result_label.pack(pady=5)

        search_button = ttk.Button(search_window, text="Search", command=perform_search, style='TButton')
        search_button.pack(pady=(10, 20))

    def update_password(self):
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Password")
        update_window.geometry("300x200")
        update_window.configure(background='#ecf0f1')

        update_label = ttk.Label(update_window, text="Enter Website:", background='#ecf0f1')
        update_label.pack(pady=(20, 10))

        update_entry = ttk.Entry(update_window, width=25)
        update_entry.pack(pady=(0, 10))

        new_password_label = ttk.Label(update_window, text="Enter New Password:", background='#ecf0f1')
        new_password_label.pack(pady=(10, 10))

        new_password_entry = ttk.Entry(update_window, show="*", width=25)
        new_password_entry.pack(pady=(0, 10))

        def perform_update():
            website = update_entry.get()
            new_password = new_password_entry.get()

            if website and new_password:
                encrypted_password = self.encryption.encrypt(new_password)
                self.db.update_password({"website": website}, {"password": encrypted_password})
                self.update_status(f"Password for {website} updated successfully!")
                update_window.destroy()
            else:
                self.update_status("Please fill out all fields.")

        update_button = ttk.Button(update_window, text="Update Password", command=perform_update, style='TButton')
        update_button.pack(pady=(10, 20))

    def delete_password(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Password")
        delete_window.geometry("300x150")
        delete_window.configure(background='#ecf0f1')

        delete_label = ttk.Label(delete_window, text="Enter Website:", background='#ecf0f1')
        delete_label.pack(pady=(20, 10))

        delete_entry = ttk.Entry(delete_window, width=25)
        delete_entry.pack(pady=(0, 10))

        def perform_delete():
            website = delete_entry.get()
            result = self.db.delete_password({"website": website})
            if result.deleted_count > 0:
                self.update_status(f"Password for {website} deleted.")
            else:
                self.update_status("Website not found.")
            delete_window.destroy()

        delete_button = ttk.Button(delete_window, text="Delete", command=perform_delete, style='TButton')
        delete_button.pack(pady=(10, 20))

    def export_passwords(self):
        passwords = self.db.get_all_passwords()
        with open("passwords_backup.txt", "w") as file:
            for pwd in passwords:
                decrypted_password = self.encryption.decrypt(pwd['password'])
                file.write(f"Website: {pwd['website']} | Password: {decrypted_password}\n")
        self.update_status("Passwords exported to passwords_backup.txt!")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
