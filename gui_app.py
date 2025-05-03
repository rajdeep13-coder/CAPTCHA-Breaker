import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageOps
from ocr_solver import CaptchaSolver
import logging

logging.basicConfig(level=logging.INFO)

class CaptchaGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CAPTCHA Breaker")
        self.geometry("400x300")
        self.solver = CaptchaSolver()
        self._create_widgets()

    def _create_widgets(self):
        self.img_label = ttk.Label(self)
        self.img_label.pack(pady=10)
        
        self.result_var = tk.StringVar(value="")
        result_frame = ttk.Frame(self)
        ttk.Label(result_frame, text="Result:").pack(side=tk.LEFT)
        ttk.Label(result_frame, textvariable=self.result_var, font=('Helvetica', 12)).pack(side=tk.LEFT)
        result_frame.pack(pady=10)
        
        ttk.Button(self, text="Open Image", command=self._load_image).pack(pady=10)
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN).pack(side=tk.BOTTOM, fill=tk.X)

    def _load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg"), ("All Files", "*.*")])
        if path:
            self.status_var.set("Processing...")
            self.update_idletasks()
            try:
                text, conf = self.solver.solve(path)
                self.result_var.set(f"{text} (Confidence: {conf:.1f}%)")
                self._show_image(path)
                self.status_var.set("Ready")
            except Exception as e:
                self.status_var.set("Error processing image")
                logging.error(str(e))

    def _show_image(self, path):
        img = Image.open(path)
        img.thumbnail((300, 100), Image.LANCZOS)
        img = ImageOps.exif_transpose(img)
        photo = ImageTk.PhotoImage(img)
        self.img_label.configure(image=photo)
        self.img_label.image = photo

if __name__ == "__main__":
    app = CaptchaGUI()
    app.mainloop()
