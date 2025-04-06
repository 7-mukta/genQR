import random
import string
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode

class SpecialIDGenerator:
    def __init__(self, use_date=True, id_length=6):  # Change _init_ to __init__
        self.use_date = use_date
        self.id_length = id_length
        self.generated_ids = set()

    def _get_initials(self, name):
        return ''.join([part[0].upper() for part in name.strip().split()])

    def _generate_random_part(self):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=self.id_length))

    def generate_id(self, name):
        initials = self._get_initials(name)
        date_str = datetime.now().strftime("%Y%m%d") if self.use_date else ""
        unique_part = self._generate_random_part()
        special_id = f"{initials}-{date_str}-{unique_part}"

        while special_id in self.generated_ids:
            unique_part = self._generate_random_part()
            special_id = f"{initials}-{date_str}-{unique_part}"

        self.generated_ids.add(special_id)
        return special_id

class SpecialIDApp:
    def __init__(self, root):  # Change _init_ to __init__
        self.generator = SpecialIDGenerator()
        self.root = root
        self.root.title("Special ID Generator with QR Code")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # Styling
        self.root.configure(bg="#f2f2f2")
        font_large = ("Helvetica", 14)
        font_small = ("Helvetica", 10)

        # Widgets
        self.label = tk.Label(root, text="Enter your full name:", bg="#f2f2f2", font=font_large)
        self.label.pack(pady=10)

        self.name_entry = tk.Entry(root, width=30, font=font_small)
        self.name_entry.pack(pady=5)

        self.generate_button = tk.Button(root, text="Generate ID", command=self.generate_id, font=font_small, bg="#4CAF50", fg="white", width=20)
        self.generate_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", bg="#f2f2f2", font=("Helvetica", 12, "bold"))
        self.result_label.pack(pady=10)

        self.qr_label = tk.Label(root, bg="#f2f2f2")
        self.qr_label.pack(pady=10)

    def generate_id(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter your name.")
            return

        special_id = self.generator.generate_id(name)
        self.result_label.config(text=f"Your Special ID: {special_id}")

        self.generate_qr_code(special_id)

    def generate_qr_code(self, data):
        # Generate QR
        qr = qrcode.make(data)
        qr = qr.resize((200, 200))

        # Convert to Tkinter-compatible image
        self.qr_image = ImageTk.PhotoImage(qr)
        self.qr_label.config(image=self.qr_image)

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = SpecialIDApp(root)
    root.mainloop()
