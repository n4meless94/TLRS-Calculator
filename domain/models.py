
from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

@dataclass
class Holiday:
    date: date
    name: str = "Public Holiday"
    is_observed: bool = False
    source: str = "fetched"  # fetched, manual, cache

@dataclass
class CalculationResult:
    grade: str
    rate: int
    year: int
    month: int
    
    # Counts
    total_days_in_month: int
    working_days_count: int
    weekend_days_count: int
    public_holidays_count: int
    personal_leave_count: int
    
    # Details
    holidays: List[Holiday] = field(default_factory=list)
    working_days: List[date] = field(default_factory=list)
    leave_days: List[date] = field(default_factory=list)
    ignored_leave_dates: List[date] = field(default_factory=list)
    
    # Money
    total_reimbursement: int = 0
    
    @property
    def period_label(self) -> str:
        import calendar
        return f"{calendar.month_name[self.month]} {self.year}"

    @property
    def ignored_leave_count(self) -> int:
        return len(self.ignored_leave_dates)
