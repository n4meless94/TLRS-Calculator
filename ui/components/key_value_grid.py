
import tkinter as tk
from tkinter import ttk
from ui.styles import *

class KeyValueGrid(ttk.Frame):
    def __init__(self, parent, data=None):
        super().__init__(parent)
        self.data = data or {}
        self.rows = []
        self._build_grid()
        
    def _build_grid(self):
        # Clear existing
        for widget in self.winfo_children():
            widget.destroy()
            
        row_idx = 0
        for key, value in self.data.items():
            # Key
            k = tk.Label(
                self, 
                text=key + ":", 
                font=("Segoe UI", 9, "bold"), 
                bg=COLOR_LIGHT_BG if row_idx % 2 == 0 else COLOR_WHITE,
                anchor="e",
                width=20
            )
            k.grid(row=row_idx, column=0, sticky="ew", padx=1, pady=1)
            
            # Value
            v = tk.Label(
                self, 
                text=str(value), 
                font=("Segoe UI", 9),
                bg=COLOR_LIGHT_BG if row_idx % 2 == 0 else COLOR_WHITE,
                anchor="w"
            )
            v.grid(row=row_idx, column=1, sticky="ew", padx=1, pady=1, ipadx=5)
            
            row_idx += 1
            
        self.columnconfigure(1, weight=1)
        
    def update_data(self, new_data):
        self.data = new_data
        self._build_grid()
