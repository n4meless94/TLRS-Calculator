
import csv
from domain.models import CalculationResult

class CsvExporter:
    def __init__(self, result: CalculationResult):
        self.result = result

    def export(self, filename: str):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(["TLRS Report", f"{self.result.year}-{self.result.month:02d}"])
            writer.writerow(["Grade", self.result.grade])
            writer.writerow(["Rate", self.result.rate])
            writer.writerow(["Working Days", self.result.working_days_count])
            writer.writerow(["Total Reimbursement", self.result.total_reimbursement])
            writer.writerow([])
            
            # Details
            writer.writerow(["Date", "Day", "Status", "Note"])
            
            # Reconstruct timeline
            import calendar
            import datetime as dt
            
            holidays_map = {h.date: h.name for h in self.result.holidays}
            leave_set = set(self.result.leave_days)
            working_set = set(self.result.working_days)
            
            num_days = calendar.monthrange(self.result.year, self.result.month)[1]
            for day in range(1, num_days + 1):
                d = dt.date(self.result.year, self.result.month, day)
                status = "Excluded"
                note = ""
                
                if d in holidays_map:
                    status = "Public Holiday"
                    note = holidays_map[d]
                elif d in leave_set:
                    status = "Personal Leave"
                elif d.weekday() >= 5:
                    status = "Weekend"
                elif d in working_set:
                    status = "Working Day"
                    
                writer.writerow([d, d.strftime("%A"), status, note])
