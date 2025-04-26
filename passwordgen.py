import string
import random
import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip  # For clipboard functionality
import os
from datetime import datetime

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("400x400")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Length selection
        ttk.Label(self.root, text="Random Password Length:").pack(pady=5)
        self.length_var = tk.IntVar(value=12)
        self.length_spin = ttk.Spinbox(
            self.root, from_=8, to=64, textvariable=self.length_var, width=5
        )
        self.length_spin.pack()
        
        # Complexity options
        ttk.Label(self.root, text="Include:").pack(pady=5)
        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(self.root, text="Lowercase", variable=self.lower_var).pack()
        ttk.Checkbutton(self.root, text="Uppercase", variable=self.upper_var).pack()
        ttk.Checkbutton(self.root, text="Digits", variable=self.digits_var).pack()
        ttk.Checkbutton(self.root, text="Symbols", variable=self.symbols_var).pack()
        
        # Generate button
        ttk.Button(self.root, text="Generate Password", command=self.generate_password).pack(pady=10)
        
        # Password display
        self.password_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.password_var, state="readonly", width=30, font=('Arial', 10)).pack(pady=5)
        
        # Action buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        # Copy to clipboard and save buttons
        ttk.Button(btn_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Save to File", command=self.save_password).pack(side=tk.LEFT, padx=5)
    
    def generate_password(self):
        char_sets = {
            'lower': string.ascii_lowercase if self.lower_var.get() else '',
            'upper': string.ascii_uppercase if self.upper_var.get() else '',
            'digits': string.digits if self.digits_var.get() else '',
            'symbols': string.punctuation if self.symbols_var.get() else ''
        }
        
        all_chars = ''.join(char_sets.values())
        
        if not all_chars:
            messagebox.showerror("Error", "Please select at least one character type")
            return
        
        length = self.length_var.get()
        password = ''.join(random.choices(all_chars, k=length))
        self.password_var.set(password)
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password generated yet")
    
    def save_password(self):
        password = self.password_var.get()
        if not password:
            messagebox.showwarning("Warning", "No password generated yet")
            return
        
        save_dir = "saved_passwords"
        os.makedirs(save_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{save_dir}/password_{timestamp}.txt"
        
        try:
            with open(filename, "w") as f:
                f.write(f"Password generated on {timestamp}\n")
                f.write(f"Password: {password}\n")
            
            messagebox.showinfo("Success", f"Password saved to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save password:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()