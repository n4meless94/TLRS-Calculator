
import tkinter as tk
from tkinter import ttk
from ui.styles import *

class HeroCard(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Frame style/border
        self.frame = tk.Frame(self, bg=COLOR_ACCENT, padx=2, pady=2)
        self.frame.pack(fill=tk.X, expand=True)
        
        self.inner = tk.Frame(self.frame, bg=COLOR_WHITE, padx=20, pady=15)
        self.inner.pack(fill=tk.X, expand=True)
        
        # Top label
        self.lbl_title = tk.Label(
            self.inner, 
            text="Total Reimbursement", 
            font=FONT_NORMAL, 
            bg=COLOR_WHITE, 
            fg=COLOR_SECONDARY
        )
        self.lbl_title.pack(anchor=tk.W)
        
        # Amount
        self.lbl_amount = tk.Label(
            self.inner,
            text="RM 0.00",
            font=FONT_HERO,
            bg=COLOR_WHITE,
            fg=COLOR_ACCENT
        )
        self.lbl_amount.pack(anchor=tk.W)
        
        # Detail line
        self.lbl_detail = tk.Label(
            self.inner,
            text="0 eligible days × RM 0/day",
            font=FONT_SMALL,
            bg=COLOR_WHITE,
            fg="#7f8c8d"
        )
        self.lbl_detail.pack(anchor=tk.W)
        
    def update_value(self, total: int, days: int, rate: int):
        self.lbl_amount.config(text=f"RM {total:,.2f}")
        self.lbl_detail.config(text=f"{days} eligible days × RM{rate}/day")
