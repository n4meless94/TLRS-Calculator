
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime as dt
import calendar
import queue
import threading
from typing import Set, Dict, Optional

from domain.models import CalculationResult, Holiday
from domain.calculator import calculate_period, GRADE_RATES
from services.holiday_service import HolidayService
from exporters.excel_exporter import ExcelExporter
from exporters.csv_exporter import CsvExporter
from exporters.pdf_exporter import PdfExporter

from ui.styles import *
from ui.components.hero_card import HeroCard
from ui.components.key_value_grid import KeyValueGrid
from ui.components.log_viewer import LogViewer


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("QSB Working Day Calendar (TLRS) v2.0")
        self.root.geometry("1100x750")
        
        # Services
        self.holiday_service = HolidayService()
        self.holiday_queue = queue.Queue()
        
        # State
        self.holidays_map: Dict[dt.date, str] = {}
        self.holiday_source: str = "None"
        self.leave_dates: Set[dt.date] = set()
        self.current_result: Optional[CalculationResult] = None
        
        # UI
        self._setup_styles()
        self._build_ui()
        
        # Start async fetch for current year
        self.refresh_holidays()
        
        # Start queue poller
        self.root.after(100, self._process_queue)

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=COLOR_LIGHT_BG)
        style.configure("TLabel", background=COLOR_LIGHT_BG, font=FONT_NORMAL)
        style.configure("TButton", font=FONT_NORMAL)
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), background=COLOR_ACCENT, foreground=COLOR_WHITE)
        
    def nav_prev(self):
        m = self.month_var.get()
        y = self.year_var.get()
        if m == 1:
            self.month_var.set(12)
            self.year_var.set(y - 1)
        else:
            self.month_var.set(m - 1)
        self._update_combo_from_var()

    def nav_next(self):
        m = self.month_var.get()
        y = self.year_var.get()
        if m == 12:
            self.month_var.set(1)
            self.year_var.set(y + 1)
        else:
            self.month_var.set(m + 1)
        self._update_combo_from_var()

    def preview_nav_prev(self):
        print("DEBUG: MainWindow preview_nav_prev called")
        self.nav_prev()
        self.calculate()
        
    def preview_nav_next(self):
        print("DEBUG: MainWindow preview_nav_next called")
        self.nav_next()
        self.calculate()

    def _build_ui(self):
        main_container = ttk.Frame(self.root, padding=PADDING_LARGE)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # === Header ===
        header = ttk.Frame(main_container)
        header.pack(fill=tk.X, pady=(0, PADDING_LARGE))
        tk.Label(header, text="QSB TLRS Calculator", font=FONT_TITLE, bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY).pack(side=tk.LEFT)
        self.status_lbl = tk.Label(header, text="Ready", font=FONT_SMALL, bg=COLOR_LIGHT_BG, fg="#7f8c8d")
        self.status_lbl.pack(side=tk.RIGHT, pady=5)

        # === Content Split ===
        content = ttk.Frame(main_container)
        content.pack(fill=tk.BOTH, expand=True)

        # --- Left Panel (Inputs) ---
        left = ttk.Frame(content, width=350)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, PADDING_LARGE))
        
        # Grade Selection
        grade_frame = ttk.LabelFrame(left, text="Grade", padding=PADDING_NORMAL)
        grade_frame.pack(fill=tk.X, pady=(0, PADDING_NORMAL))
        
        self.grade_var = tk.StringVar(value="JG6")
        grades = list(GRADE_RATES.keys())
        for i, grade in enumerate(grades):
            rb = ttk.Radiobutton(grade_frame, text=f"{grade} (RM{GRADE_RATES[grade]})", variable=self.grade_var, value=grade)
            rb.grid(row=i//2, column=i%2, sticky="w", padx=5, pady=2)

        # Period Selection
        period_frame = ttk.LabelFrame(left, text="Period", padding=PADDING_NORMAL)
        period_frame.pack(fill=tk.X, pady=(0, PADDING_NORMAL))
        
        f_period = ttk.Frame(period_frame)
        f_period.pack(fill=tk.X)

        # Layout: [ < ] [ Month Combo ] [ Year ] [ > ] [Today]
        
        btn_prev = ttk.Button(f_period, text="<", width=3, command=self.nav_prev)
        btn_prev.pack(side=tk.LEFT, padx=(0, 2))
        
        self.month_var = tk.IntVar(value=dt.date.today().month)
        self.year_var = tk.IntVar(value=dt.date.today().year)
        
        months = [f"{i} - {calendar.month_name[i]}" for i in range(1, 13)]
        self.cb_month = ttk.Combobox(f_period, values=months, state="readonly", width=12) # Slightly smaller width
        self.cb_month.current(self.month_var.get()-1)
        self.cb_month.bind("<<ComboboxSelected>>", lambda e: self.month_var.set(self.cb_month.current()+1))
        self.cb_month.pack(side=tk.LEFT, padx=2)
        
        sb_year = ttk.Spinbox(f_period, from_=2020, to=2030, textvariable=self.year_var, width=6)
        sb_year.pack(side=tk.LEFT, padx=2)
        
        btn_next = ttk.Button(f_period, text=">", width=3, command=self.nav_next)
        btn_next.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_today = ttk.Button(f_period, text="Today", command=self._set_today, width=6)
        btn_today.pack(side=tk.LEFT)

        # Personal Leave
        leave_frame = ttk.LabelFrame(left, text="Personal Leave", padding=PADDING_NORMAL)
        leave_frame.pack(fill=tk.X, pady=(0, PADDING_NORMAL))
        
        tk.Label(leave_frame, text="Dates (YYYY-MM-DD or DD/MM/YYYY):", bg=COLOR_LIGHT_BG).pack(anchor="w")
        self.txt_leave = tk.Text(leave_frame, height=4, width=30, font=FONT_MONO)
        self.txt_leave.pack(fill=tk.X, pady=5)
        
        # Calculate Button
        self.btn_calc = ttk.Button(left, text="Calculate Reimbursement", command=self.calculate, style="Accent.TButton")
        self.btn_calc.pack(fill=tk.X, pady=PADDING_NORMAL)
        
        # --- Right Panel (Results) ---
        right = ttk.Frame(content)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Init Settings Service FIRST
        from services.settings_service import SettingsService
        self.settings_service = SettingsService()
        
        # Hero Card
        self.hero = HeroCard(right)
        self.hero.pack(fill=tk.X, pady=(0, PADDING_NORMAL))
        
        # Tabs
        self.notebook = ttk.Notebook(right)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Summary Tab
        tab_summary = ttk.Frame(self.notebook, padding=PADDING_NORMAL)
        self.notebook.add(tab_summary, text="Summary")
        
        self.kv_grid = KeyValueGrid(tab_summary)
        self.kv_grid.pack(fill=tk.X, anchor="n")
        
        # Details Tab
        self.txt_details = tk.Text(self.notebook, font=FONT_MONO)
        self.notebook.add(self.txt_details, text="Full Report")
        
        # Logs Tab (Conditional)
        self.log_viewer = LogViewer(self.notebook)
        if self.settings_service.get("developer_mode"):
            self.notebook.add(self.log_viewer, text="Logs (Debug)")
        
        # PDF Preview Tab
        from ui.components.pdf_preview import PdfPreview
        import tempfile
        import os
        
        self.pdf_preview = PdfPreview(self.notebook, on_prev=self.preview_nav_prev, on_next=self.preview_nav_next)
        self.notebook.add(self.pdf_preview, text="PDF Preview")
        # Bind tab change to auto-refresh preview when selected
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        
        # Settings Tab
        # from services.settings_service import SettingsService (Already init at top)
        # self.settings_service = SettingsService()
        
        # Apply Default Grade
        def_grade = self.settings_service.get("default_grade")
        if def_grade in list(GRADE_RATES.keys()):
            self.grade_var.set(def_grade)
            
        tab_settings = ttk.Frame(self.notebook, padding=PADDING_NORMAL)
        self.notebook.add(tab_settings, text="Settings")
        
        # Settings UI
        lbl_title = tk.Label(tab_settings, text="Application Settings", font=FONT_TITLE, bg=COLOR_LIGHT_BG)
        lbl_title.pack(anchor="w", pady=(0, 5))
        
        lbl_subtitle = tk.Label(tab_settings, text="(Changes are saved automatically)", font=("Helvetica", 9, "italic"), bg=COLOR_LIGHT_BG, fg=COL_TEXT_MUTED)
        lbl_subtitle.pack(anchor="w", pady=(0, 20))
        
        # 1. Default Grade
        f_grade = ttk.LabelFrame(tab_settings, text="Default Grade", padding=PADDING_NORMAL)
        f_grade.pack(fill=tk.X, pady=(0, 10))
        
        lbl_g = tk.Label(f_grade, text="Select the grade selected by default when app starts:", bg=COLOR_LIGHT_BG)
        lbl_g.pack(anchor="w", pady=(0, 5))
        
        self.var_def_grade = tk.StringVar(value=def_grade)
        cb_def_grade = ttk.Combobox(f_grade, values=list(GRADE_RATES.keys()), textvariable=self.var_def_grade, state="readonly")
        cb_def_grade.pack(anchor="w")
        
        def save_grade(e):
            self.settings_service.set("default_grade", self.var_def_grade.get())
        cb_def_grade.bind("<<ComboboxSelected>>", save_grade)
        
        # 2. Export Prefs
        f_export = ttk.LabelFrame(tab_settings, text="Export Preferences", padding=PADDING_NORMAL)
        f_export.pack(fill=tk.X, pady=(0, 10))
        
        self.var_auto_open = tk.BooleanVar(value=self.settings_service.get("auto_open_export"))
        def save_auto_open():
            self.settings_service.set("auto_open_export", self.var_auto_open.get())
            
        chk_open = ttk.Checkbutton(f_export, text="Automatically open files after exporting", variable=self.var_auto_open, command=save_auto_open)
        chk_open.pack(anchor="w")
        
        # 3. Data Management
        f_data = ttk.LabelFrame(tab_settings, text="Data Management", padding=PADDING_NORMAL)
        f_data.pack(fill=tk.X, pady=(0, 10))
        
        def clear_cache():
            # Delete json files in cache dir
            import glob
            count = 0
            for p in self.holiday_service.get_cache_path(2000).parent.glob("holiday_cache_*.json"):
                try:
                    p.unlink()
                    count += 1
                except: pass
            messagebox.showinfo("Cache Cleared", f"Deleted {count} cache file(s).\nPlease click 'Refresh Holidays' to re-download data.")
            
        btn_clear = ttk.Button(f_data, text="Clear Holiday Cache", command=clear_cache)
        btn_clear.pack(anchor="w")

        # 4. Display Settings
        f_disp = ttk.LabelFrame(tab_settings, text="Display Settings", padding=PADDING_NORMAL)
        f_disp.pack(fill=tk.X, pady=(0, 10))
        
        self.var_dev_mode = tk.BooleanVar(value=self.settings_service.get("developer_mode"))
        def toggle_dev():
            val = self.var_dev_mode.get()
            self.settings_service.set("developer_mode", val)
            
            # Toggle Tab
            if val:
                # Add back at index 2 (after Summary[0] and Report[1])
                try:
                    self.notebook.insert(2, self.log_viewer, text="Logs (Debug)")
                except:
                    self.notebook.add(self.log_viewer, text="Logs (Debug)") # Fallback
            else:
                try:
                    self.notebook.forget(self.log_viewer)
                except: pass
                
        chk_dev = ttk.Checkbutton(f_disp, text="Developer Mode (Show Debug Logs)", variable=self.var_dev_mode, command=toggle_dev)
        chk_dev.pack(anchor="w")
        
        # About Tab
        tab_about = ttk.Frame(self.notebook, padding=PADDING_LARGE)
        self.notebook.add(tab_about, text="About")
        
        # Container
        container = ttk.Frame(tab_about)
        container.pack(expand=True, fill=tk.BOTH)
        
        # Header Section
        lbl_app = tk.Label(container, text="QSB Working Day Calendar", font=("Segoe UI", 24, "bold"), bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)
        lbl_app.pack(pady=(40, 5))
        
        lbl_ver = tk.Label(container, text="Version 1.0", font=("Segoe UI", 12), bg=COLOR_LIGHT_BG, fg=COL_TEXT_MUTED)
        lbl_ver.pack(pady=(0, 30))
        
        # Divider
        ttk.Separator(container, orient="horizontal").pack(fill=tk.X, padx=100, pady=10)
        
        # Info Section
        info_frame = ttk.Frame(container)
        info_frame.pack(pady=20)
        
        def add_info_row(label, value):
            row = ttk.Frame(info_frame)
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=label, font=("Segoe UI", 10, "bold"), width=15, anchor="e", bg=COLOR_LIGHT_BG).pack(side=tk.LEFT, padx=(0, 10))
            tk.Label(row, text=value, font=FONT_NORMAL, anchor="w", bg=COLOR_LIGHT_BG).pack(side=tk.LEFT)
            
        add_info_row("Developer:", "Qhazanah Sabah Berhad (IT Dept)")
        add_info_row("Module:", "TLRS Reimbursement Calculator")
        add_info_row("Framework:", "Python 3.12 + Tkinter")
        add_info_row("PDF Engine:", "ReportLab + PyMuPDF")
        
        # Footer
        lbl_copy = tk.Label(container, text="© 2026 Qhazanah Sabah Berhad. All rights reserved.", font=FONT_SMALL, bg=COLOR_LIGHT_BG, fg="#999")
        lbl_copy.pack(side=tk.BOTTOM, pady=20)

        # Export Buttons
        btn_frame = ttk.Frame(right)
        btn_frame.pack(fill=tk.X, pady=PADDING_NORMAL)
        
        ttk.Button(btn_frame, text="Export Excel", command=self.export_excel).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Export CSV", command=self.export_csv).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Export PDF", command=self.export_pdf).pack(side=tk.LEFT)
        
        self.btn_refresh = ttk.Button(btn_frame, text="Refresh Holidays", command=lambda: self.refresh_holidays(force=True))
        self.btn_refresh.pack(side=tk.RIGHT)



    def _set_today(self):
        today = dt.date.today()
        self.month_var.set(today.month)
        self.year_var.set(today.year)
        self._update_combo_from_var()

    def _update_combo_from_var(self):
        # Sync combobox with variable (0-based index vs 1-based month)
        current_m = self.month_var.get()
        if 1 <= current_m <= 12:
            self.cb_month.current(current_m - 1)
        
    def refresh_holidays(self, force=False):
        year = self.year_var.get()
        self.status_lbl.config(text=f"Fetching holidays for {year}...", fg=COLOR_WARNING)
        self.btn_refresh.config(state="disabled")
        
        self.holiday_service.fetch_holidays_async(
            year,
            self._on_holiday_success,
            self._on_holiday_error,
            force_refresh=force
        )
        
    def _on_holiday_success(self, holidays, source):
        self.holiday_queue.put(("success", holidays, source))

    def _on_holiday_error(self, error):
        self.holiday_queue.put(("error", error))

    def _process_queue(self):
        try:
            while True:
                msg = self.holiday_queue.get_nowait()
                status = msg[0]
                if status == "success":
                    self.holidays_map = msg[1]
                    self.holiday_source = msg[2]
                    self.status_lbl.config(text=f"Holidays loaded ({self.holiday_source})", fg=COLOR_ACCENT)
                elif status == "error":
                    self.status_lbl.config(text=f"Error: {msg[1]}", fg=COLOR_ERROR)
                    messagebox.showerror("Holiday Fetch Error", msg[1])
                
                self.btn_refresh.config(state="normal")
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self._process_queue)


    def _on_tab_changed(self, event):
        # Check if selected tab is PDF Preview
        try:
            selected_tab_id = self.notebook.select()
            tab_text = self.notebook.tab(selected_tab_id, "text")
            
            if tab_text == "PDF Preview":
                self._refresh_pdf_preview()
        except:
            pass

    def _refresh_pdf_preview(self):
        if not self.current_result:
            self.pdf_preview.show_message("Please calculate reimbursement first.")
            return
            
        try:
            # Generate to temp file
            import tempfile
            import os
            
            fd, path = tempfile.mkstemp(suffix=".pdf")
            os.close(fd)
            
            # Generate
            exporter = PdfExporter(self.current_result, self.holiday_source)
            exporter.export(path)
            
            # Render
            self.pdf_preview.render_pdf(path)
            
            # Clean up? PyMuPDF might lock it? 
            # We'll leave it in temp for now or try to delete later.
            # OS should handle temp cleanup eventually.
            
        except Exception as e:
            self.pdf_preview.show_message(f"Preview Error: {str(e)}")

    def calculate(self):
        # 1. Parse Leave
        raw_leave = self.txt_leave.get("1.0", tk.END).strip()
        self.leave_dates = set()
        if raw_leave:
            import re
            # Split by comma or newline
            parts = re.split(r'[,\n]', raw_leave)
            for p in parts:
                p = p.strip()
                if not p: continue
                # Parse date logic (simple fallback for now)
                try:
                    # try ISO first
                    d = dt.date.fromisoformat(p)
                    self.leave_dates.add(d)
                except:
                    # try DMY
                    try:
                        d = dt.datetime.strptime(p, "%d/%m/%Y").date()
                        self.leave_dates.add(d)
                    except:
                        pass # Ignore invalid

        # 2. Run Calc
        try:
            result = calculate_period(
                year=self.year_var.get(),
                month=self.month_var.get(),
                grade=self.grade_var.get(),
                holidays_map=self.holidays_map,
                leave_dates=self.leave_dates
            )
            self.current_result = result
            self._update_display(result)
        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))

    def _update_display(self, res: CalculationResult):
        # Hero
        self.hero.update_value(res.total_reimbursement, res.working_days_count, res.rate)
        
        # Grid
        self.kv_grid.update_data({
            "Grade": res.grade,
            "Rate": f"RM {res.rate}",
            "Total Days": res.total_days_in_month,
            "Working Days": res.working_days_count,
            "Weekends": res.weekend_days_count,
            "Public Holidays": res.public_holidays_count,
            "Personal Leave": res.personal_leave_count,
            "Ignored Leave": res.ignored_leave_count
        })
        
        # Details Text (Quick view)
        lines = []
        lines.append(f"Report for {res.period_label}")
        lines.append("-" * 40)
        lines.append("HOLIDAYS:")
        for h in res.holidays:
            obs = " (Observed)" if h.is_observed else ""
            lines.append(f"  {h.date.strftime('%d/%m/%Y')}: {h.name}{obs}")
        lines.append("")
        lines.append("LEAVE DEDUCTED:")
        for d in res.leave_days:
            lines.append(f"  {d.strftime('%d/%m/%Y')}")
        
        self.txt_details.delete("1.0", tk.END)
        self.txt_details.insert("1.0", "\n".join(lines))
        
        # Real-time PDF Preview Update
        try:
            selected_tab_id = self.notebook.select()
            if self.notebook.tab(selected_tab_id, "text") == "PDF Preview":
                self._refresh_pdf_preview()
        except:
            pass
        
    def export_excel(self):
        if not self.current_result: return
        try:
            path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
            if path:
                exporter = ExcelExporter(self.current_result, self.holiday_source)
                exporter.export(path)
                
                from ui.components.modern_messagebox import ModernMessagebox
                ModernMessagebox.show_success(self.root, "Export Success", f"Successfully saved to:\n{path}")
                
                if self.settings_service.get("auto_open_export"):
                    try: os.startfile(path)
                    except: pass
        except Exception as e:
            from ui.components.modern_messagebox import ModernMessagebox
            ModernMessagebox.show_error(self.root, "Export Failed", str(e))

    def export_csv(self):
        if not self.current_result: return
        try:
            path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if path:
                exporter = CsvExporter(self.current_result)
                exporter.export(path)
                
                from ui.components.modern_messagebox import ModernMessagebox
                ModernMessagebox.show_success(self.root, "Export Success", f"Successfully saved to:\n{path}")
                
                if self.settings_service.get("auto_open_export"):
                    try: os.startfile(path)
                    except: pass
        except Exception as e:
            from ui.components.modern_messagebox import ModernMessagebox
            ModernMessagebox.show_error(self.root, "Export Failed", str(e))

    def export_pdf(self):
        if not self.current_result: return
        try:
            path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if path:
                exporter = PdfExporter(self.current_result, self.holiday_source)
                exporter.export(path)
                
                # Modern Success
                from ui.components.modern_messagebox import ModernMessagebox
                ModernMessagebox.show_success(self.root, "Export Success", f"Successfully saved to:\n{path}")
                
                if self.settings_service.get("auto_open_export"):
                    try: os.startfile(path)
                    except: pass
        except Exception as e:
            # Modern Error
            from ui.components.modern_messagebox import ModernMessagebox
            ModernMessagebox.show_error(self.root, "Export Failed", str(e))
