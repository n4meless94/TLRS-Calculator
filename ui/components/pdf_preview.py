import tkinter as tk
from tkinter import ttk
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import io

class PdfPreview(ttk.Frame):
    def __init__(self, parent, on_prev=None, on_next=None):
        super().__init__(parent)
        self.on_prev = on_prev
        self.on_next = on_next
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Canvas
        self.canvas = tk.Canvas(self, bg="#525659")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Controls Layer (Floating Buttons)
        # Use place() relative to the Frame to ensure they are always on top of the canvas
        self.btn_prev = tk.Button(self, text="❮", command=self._handle_prev, 
                                 bg="white", font=("Arial", 16, "bold"), bd=1, cursor="hand2")
        self.btn_next = tk.Button(self, text="❯", command=self._handle_next, 
                                 bg="white", font=("Arial", 16, "bold"), bd=1, cursor="hand2")
        
        # State
        self.image_ref = None
        self.current_pdf_path = None
        self.resize_timer = None
        
        # Bindings
        self.canvas.bind("<Configure>", self._on_resize)
        
    def _handle_prev(self):
        print("DEBUG: Prev clicked in PdfPreview")
        if self.on_prev: self.on_prev()
        
    def _handle_next(self):
        print("DEBUG: Next clicked in PdfPreview")
        if self.on_next: self.on_next()

    def _on_resize(self, event):
        # Reposition buttons using place (relative coordinates)
        # We don't need to manually calculate pixels for place if using relx/rely, 
        # but we want fixed pixels from edge.
        # So we update place coordinates.
        w = event.width
        h = event.height
        
        # Keep vertical center
        self.btn_prev.place(x=20, y=h//2, anchor="w", width=40, height=60)
        self.btn_next.place(x=w-20, y=h//2, anchor="e", width=40, height=60)
        
        # Debounce render
        if self.resize_timer:
            self.after_cancel(self.resize_timer)
        self.resize_timer = self.after(200, self._render_current)

    def render_pdf(self, pdf_path: str):
        self.current_pdf_path = pdf_path
        self._render_current()
        
    def _render_current(self):
        # Buttons are managed by place() in _on_resize and here
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        
        # Ensure placement
        self.btn_prev.place(x=20, y=h//2, anchor="w", width=40, height=60)
        self.btn_next.place(x=w-20, y=h//2, anchor="e", width=40, height=60)
        self.btn_prev.lift()
        self.btn_next.lift()

        if not self.current_pdf_path: return
        
        try:
            # Get available size
            # w, h from above
            if w < 50 or h < 50: return 
            
            doc = fitz.open(self.current_pdf_path)
            if len(doc) < 1: return
            page = doc.load_page(0)
            
            # Calculate Scale to FIT PAGE
            rect = page.rect
            scale_w = (w - 120) / rect.width 
            scale_h = (h - 40) / rect.height
            scale = min(scale_w, scale_h)
            
            # Render
            mat = fitz.Matrix(scale, scale)
            pix = page.get_pixmap(matrix=mat)
            
            img_data = pix.tobytes("ppm")
            pil_image = Image.open(io.BytesIO(img_data))
            self.image_ref = ImageTk.PhotoImage(pil_image)
            
            # Draw centered
            self.canvas.delete("all")
            self.canvas.create_image(
                w//2, h//2,
                image=self.image_ref,
                anchor="center"
            )
            
        except Exception as e:
            self.show_message(f"Error: {str(e)}")

    def show_message(self, text):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.create_text(
            w//2, h//2,
            text=text,
            fill="white",
            font=("Helvetica", 12),
            anchor="center"
        )
