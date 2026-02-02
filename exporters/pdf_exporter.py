
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import calendar
import datetime as dt
from domain.models import CalculationResult

class PdfExporter:
    def __init__(self, result: CalculationResult, holiday_source: str = ""):
        self.result = result
        self.holiday_source = holiday_source
        self.width, self.height = landscape(A4)
        
    def export(self, filename: str):
        c = canvas.Canvas(filename, pagesize=landscape(A4))
        
        # === COLORS & STYLES ===
        COL_TEXT = colors.HexColor("#333333")
        COL_TEXT_MUTED = colors.HexColor("#777777")
        
        # Summary Card Colors (Muted for print safety)
        COL_CARD_BG = colors.HexColor("#F9FAFB") # Very light grey for cards
        COL_CARD_BORDER = colors.HexColor("#E5E7EB")
        
        # Cell Colors ( Distinct patterns/shades for grayscale)
        COL_CELL_WORKING = colors.white
        COL_BORDER_WORKING = colors.HexColor("#E5E7EB")
        
        COL_CELL_WEEKEND = colors.HexColor("#F3F4F6") # Light Grey
        COL_BORDER_WEEKEND = colors.HexColor("#D1D5DB")
        
        COL_CELL_HOLIDAY = colors.white
        COL_BORDER_HOLIDAY = colors.HexColor("#EF4444") # Red border implies important
        
        COL_CELL_PLACEHOLDER = colors.HexColor("#FAFAFA")
        COL_BORDER_PLACEHOLDER = colors.HexColor("#EEEEEE")

        # === 1. HEADER (Compact) ===
        margin_x = 30
        cursor_y = self.height - 40
        
        # Title Left
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(COL_TEXT)
        c.drawString(margin_x, cursor_y, "TLRS Reimbursement Calendar")
        
        # Month/Year Subtitle
        c.setFont("Helvetica", 12)
        c.setFillColor(COL_TEXT_MUTED)
        month_label = f"{calendar.month_name[self.result.month]} {self.result.year}"
        c.drawString(margin_x, cursor_y - 16, month_label)
        
        # Meta Right (Moved to Footer as per feedback)
        # However, we can keep a very subtle version or just remove it if footer is enough.
        # User said "traceable in print". Footer is best.
        
        # === 2. SUMMARY CARDS (4 Column, 1 Row) ===
        cursor_y -= 40 # Gap after header
        
        # Calculate card width dynamically for 4 columns
        # Available width = Width - Margins
        # Gaps = 3 gaps between 4 cards
        gap_x = 10
        gap_y = 10
        avail_w_cards = self.width - (margin_x * 2)
        card_w = (avail_w_cards - (gap_x * 3)) / 4
        card_h = 50 # Slightly taller for better breathing room if needed, or keep 45
        
        grid_start_x = margin_x
        
        # Helper 
        def draw_stat_card(x, y, label, value, is_total=False):
            # Bg
            bg = colors.HexColor("#FFF0F5") if is_total else COL_CARD_BG
            border = colors.HexColor("#FF0055") if is_total else COL_CARD_BORDER
            
            c.setFillColor(bg)
            c.setStrokeColor(border)
            c.setLineWidth(1 if is_total else 0.5)
            c.roundRect(x, y, card_w, card_h, 6, fill=1, stroke=1)
            
            # Label
            c.setFillColor(COL_TEXT_MUTED)
            c.setFont("Helvetica", 8) # Slightly smaller label for narrower cards
            c.drawString(x + 10, y + card_h - 14, label)
            
            # Value
            c.setFillColor(COL_TEXT if not is_total else colors.HexColor("#C62828"))
            c.setFont("Courier-Bold", 12) # Slightly smaller value
            c.drawString(x + 10, y + 10, value)

        # Draw all 4 in one row
        current_y = cursor_y - card_h
        
        # 1. Grade
        draw_stat_card(margin_x, current_y, "Grade", self.result.grade)
        
        # 2. Rate (Shifted by 1 card + gap)
        draw_stat_card(margin_x + card_w + gap_x, current_y, "Rate per Day", f"RM {self.result.rate}")
        
        # 3. Eligible Days
        draw_stat_card(margin_x + (card_w + gap_x)*2, current_y, "Eligible Working Days", f"{self.result.working_days_count} days")
        
        # 4. Total
        draw_stat_card(margin_x + (card_w + gap_x)*3, current_y, "Total Reimbursement", f"RM {self.result.total_reimbursement:,.2f}", is_total=True)
        
        cursor_y = current_y - 25 # Space before calendar
        
        # === 3. CALENDAR GRID ===
        # Fixed 7-col grid. 
        # Width: Use available width minus margins
        avail_width = self.width - (margin_x * 2)
        col_w = avail_width / 7
        row_h = 55
        
        # Header Row
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(COL_TEXT)
        c.setLineWidth(0.5)
        c.setStrokeColor(colors.gray)
        
        for i, day in enumerate(days):
            x = margin_x + (i * col_w)
            c.drawCentredString(x + col_w/2, cursor_y, day)
            
        cursor_y -= 8 # Header separation
        c.line(margin_x, cursor_y, self.width - margin_x, cursor_y) # Thin divider
        cursor_y -= 5 # Gap
        
        # Grid Data
        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdayscalendar(self.result.year, self.result.month)
        num_weeks = len(weeks)
        
        # Dynamic Row Height Calculation
        # Top of grid lines (approx): cursor_y - 13
        # Bottom limit (Footer starts at 30, text touches 55): let's say 75 is safe
        grid_top = cursor_y - 13
        safe_bottom = 75 
        avail_h = grid_top - safe_bottom
        
        # flexible row height (max 55, but shrink if 6 weeks)
        row_h = min(55, avail_h / num_weeks)
        
        # Pre-calc maps
        holidays_map = {h.date: h.name for h in self.result.holidays}
        leave_map = set(self.result.leave_days)
        
        legend_items = [] # Stores (Day, Name) for footer
        holiday_cells = [] # Store (x, y, col_w, row_h) for holiday cells to draw borders later
        
        current_grid_y = cursor_y - 13 - row_h # Start drawing from top row down
        # Wait, the previous loop used 'current_grid_y = cursor_y - row_h' but cursor_y included header gaps
        # Let's align exactly with the header line
        current_grid_y = (cursor_y - 13) - row_h
        
        # === PASS 1: Draw all cell fills and borders ===
        for week in weeks:
            for i, day_num in enumerate(week):
                x = margin_x + (i * col_w)
                y = current_grid_y
                
                # Draw Cell Box
                # If padding (0), draw muted placeholder
                if day_num == 0:
                    c.setFillColor(COL_CELL_PLACEHOLDER)
                    c.setStrokeColor(COL_BORDER_PLACEHOLDER)
                    c.rect(x, y, col_w, row_h, fill=1, stroke=1)
                    continue

                date_obj = dt.date(self.result.year, self.result.month, day_num)
                
                bg = COL_CELL_WORKING
                stroke = COL_BORDER_WORKING
                type_code = "W" # Default Working Code (Explicitly set)
                
                # Logic
                if date_obj in leave_map:
                    bg = colors.HexColor("#FFFDE7") # Light yellow
                    stroke = colors.HexColor("#FBC02D")
                    type_code = "L"
                    
                elif date_obj in holidays_map:
                    bg = colors.HexColor("#FFF5F5") # Very light red
                    stroke = COL_BORDER_HOLIDAY
                    type_code = "H"
                    # Store for second pass border drawing
                    holiday_cells.append((x, y, col_w, row_h))
                    # Add to legend
                    hs = holidays_map[date_obj]
                    # Split logic for multiple holidays
                    if "/" in hs:
                        parts = [p.strip() for p in hs.split("/")]
                        for p in parts:
                             legend_items.append(f"{day_num}: {p}")
                    else:
                        legend_items.append(f"{day_num}: {hs}")
                    
                elif i >= 5: # Weekend
                    bg = COL_CELL_WEEKEND
                    stroke = COL_BORDER_WEEKEND
                    type_code = "WE"
                
                # Draw Tile (fill + border)
                c.setFillColor(bg)
                c.setStrokeColor(stroke)
                c.rect(x, y, col_w, row_h, fill=1, stroke=1)
                
                # Day Number (Left Top)
                c.setFillColor(COL_TEXT)
                c.setFont("Helvetica-Bold", 11)
                c.drawString(x + 5, y + row_h - 14, str(day_num))
                
                # Status Code (Right Top - Print Friendly)
                c.setFont("Helvetica", 8)
                c.setFillColor(COL_TEXT_MUTED)
                c.drawRightString(x + col_w - 5, y + row_h - 14, type_code)
                
                # Holiday Name (Truncated/Short reference inside tile)
                if date_obj in holidays_map:
                    c.setFillColor(colors.HexColor("#C62828"))
                    c.setFont("Helvetica", 7)
                    c.drawString(x + 5, y + 5, "Public Holiday")
                    
            current_grid_y -= row_h # Move down
        
        # === PASS 2: Draw holiday borders on top to avoid clipping ===
        c.setStrokeColor(COL_BORDER_HOLIDAY)
        c.setLineWidth(1.5)  # Slightly thicker to ensure visibility
        for (x, y, w, h) in holiday_cells:
            c.rect(x, y, w, h, fill=0, stroke=1)
        c.setLineWidth(1)  # Reset to default
            
        # === 4. FOOTER & LEGEND ===
        footer_y = 30
        c.setFont("Helvetica", 9)
        c.setFillColor(COL_TEXT)
        
        # Legend Line
        c.drawString(margin_x, footer_y + 25, "Legend: [W] Working  [WE] Weekend  [H] Holiday  [L] Leave")
        
        # Detailed Holidays
        if legend_items:
            c.setFont("Helvetica", 8)
            c.setFillColor(COL_TEXT_MUTED)
            # Join with separators
            full_text = "  |  ".join(legend_items)
            
            # Line wrap logic (basic)
            max_chars = 120
            if len(full_text) > max_chars:
                # Find best split point
                split_idx = full_text.rfind("|", 0, max_chars)
                if split_idx == -1: split_idx = max_chars
                
                line1 = full_text[:split_idx]
                line2 = full_text[split_idx+1:].strip()
                c.drawString(margin_x, footer_y + 12, f"Holidays: {line1}")
                if line2:
                    c.drawString(margin_x, footer_y + 2, f"          {line2}")
            else:
                c.drawString(margin_x, footer_y + 12, f"Holidays: {full_text}")
                
        # Meta placement (Moved from header to footer bottom right)
        timestamp = dt.datetime.now().strftime("%d/%m/%Y %H:%M")
        meta_text = f"Generated: {timestamp} | System: TLRS"
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.gray)
        c.drawRightString(self.width - margin_x, footer_y, meta_text)

        c.save()
