
import tkinter as tk
from tkinter import ttk, scrolledtext
import logging
import queue

class QueueHandler(logging.Handler):
    """
    Thread-safe logging handler that pushes records to a queue.
    """
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        try:
            msg = self.format(record)
            self.log_queue.put(msg)
        except Exception:
            self.handleError(record)

class LogViewer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.log_queue = queue.Queue()
        self._setup_ui()
        self._setup_logging()
        self.after(100, self._poll_log_queue)
        
    def _setup_ui(self):
        # Scrolled Text Area
        self.txt_log = scrolledtext.ScrolledText(
            self, 
            state='disabled', 
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#d4d4d4",
            height=10
        )
        self.txt_log.pack(fill=tk.BOTH, expand=True)
        
        # Tags for coloring
        self.txt_log.tag_config('INFO', foreground='#2ecc71')   # Green
        self.txt_log.tag_config('WARNING', foreground='#f1c40f') # Yellow
        self.txt_log.tag_config('ERROR', foreground='#e74c3c')   # Red
        self.txt_log.tag_config('CRITICAL', foreground='#e74c3c', background='#ffffff')

    def _setup_logging(self):
        # Create a custom handler that feeds our queue
        self.handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%H:%M:%S')
        self.handler.setFormatter(formatter)
        
        # Add to root logger so we catch EVERYTHING
        logging.getLogger().addHandler(self.handler)
        logging.getLogger().setLevel(logging.INFO)

    def _poll_log_queue(self):
        while True:
            try:
                msg = self.log_queue.get_nowait()
                self._append_log(msg)
            except queue.Empty:
                break
        self.after(100, self._poll_log_queue)

    def _append_log(self, msg):
        self.txt_log.config(state='normal')
        
        # Determine tag
        tag = 'INFO'
        if '[WARNING]' in msg: tag = 'WARNING'
        elif '[ERROR]' in msg: tag = 'ERROR'
        elif '[CRITICAL]' in msg: tag = 'CRITICAL'
        
        self.txt_log.insert(tk.END, msg + "\n", tag)
        self.txt_log.see(tk.END) # Auto-scroll
        self.txt_log.config(state='disabled')
