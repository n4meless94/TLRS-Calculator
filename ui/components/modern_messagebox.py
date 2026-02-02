import tkinter as tk
from tkinter import ttk
from ui.styles import *

class ModernMessagebox(tk.Toplevel):
    def __init__(self, parent, title, message, mode="info"):
        super().__init__(parent)
        self.withdraw() # Hide initially
        
        self.title(title)
        self.overrideredirect(True) # Remove native window decorations
        self.configure(bg=COLOR_WHITE)
        
        # Dimensions
        w = 400
        h = 180
        
        # Center relative to parent
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (w // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        
        # Border Frame (Accent Color)
        border_color = COLOR_ACCENT if mode == "info" else COLOR_ERROR
        border = tk.Frame(self, bg=border_color, padx=2, pady=2)
        border.pack(fill=tk.BOTH, expand=True)
        
        # Main Content
        content = tk.Frame(border, bg=COLOR_WHITE)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(content, bg=COLOR_LIGHT_BG, height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        lbl_title = tk.Label(header, text=title, font=("Segoe UI", 11, "bold"), bg=COLOR_LIGHT_BG, fg=COL_TEXT)
        lbl_title.pack(side=tk.LEFT, padx=15)
        
        # Close 'X'
        btn_close = tk.Label(header, text="✕", font=("Arial", 10), bg=COLOR_LIGHT_BG, fg="#999")
        btn_close.pack(side=tk.RIGHT, padx=10)
        btn_close.bind("<Button-1>", lambda e: self.destroy())
        btn_close.bind("<Enter>", lambda e: btn_close.config(fg=COLOR_ERROR))
        btn_close.bind("<Leave>", lambda e: btn_close.config(fg="#999"))
        
        # Icon & Message Container
        body = tk.Frame(content, bg=COLOR_WHITE, padding=20)
        body.pack(fill=tk.BOTH, expand=True)
        
        # Icon (Simple text header substitute or unicode char)
        icon_char = "✓" if mode == "info" else "!"
        icon_color = COLOR_ACCENT if mode == "info" else COLOR_ERROR
        
        lbl_icon = tk.Label(body, text=icon_char, font=("Segoe UI", 24), bg=COLOR_WHITE, fg=icon_color)
        lbl_icon.pack(side=tk.LEFT, padx=(0, 15), anchor="n")
        
        # Message Text
        lbl_msg = tk.Label(body, text=message, font=FONT_NORMAL, bg=COLOR_WHITE, fg=COL_TEXT, 
                          wraplength=280, justify="left")
        lbl_msg.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Button Bar
        btn_bar = tk.Frame(content, bg=COLOR_WHITE, pady=15)
        btn_bar.pack(fill=tk.X)
        
        btn_ok = tk.Button(btn_bar, text="OK", command=self.destroy,
                          bg=COLOR_ACCENT, fg="white", font=("Segoe UI", 9, "bold"),
                          bd=0, padx=20, pady=5, cursor="hand2")
        btn_ok.pack()
        
        self.deiconify()
        self.transient(parent)
        self.grab_set()
        self.wait_window()

    @staticmethod
    def show_success(parent, title, message):
        ModernMessagebox(parent, title, message, mode="info")
        
    @staticmethod
    def show_error(parent, title, message):
        ModernMessagebox(parent, title, message, mode="error")
