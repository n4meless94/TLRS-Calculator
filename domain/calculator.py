
import calendar
import datetime as dt
from typing import List, Set, Dict, Optional
from domain.models import CalculationResult, Holiday

GRADE_RATES = {
    "JG5": 50,
    "JG6": 100,
    "JG7": 150,
    "JG8": 200,
    "JGB": 200,
    "JGA": 250,
}

def is_weekend(date: dt.date) -> bool:
    """Returns True if Saturday (5) or Sunday (6)."""
    return date.weekday() >= 5

def get_days_in_month(year: int, month: int) -> List[dt.date]:
    """Return list of all dates in the given month."""
    num_days = calendar.monthrange(year, month)[1]
    return [dt.date(year, month, day) for day in range(1, num_days + 1)]

def apply_observed_rule(holidays_map: Dict[dt.date, str]) -> Dict[dt.date, Holiday]:
    """
    Apply Sabah rule: Sunday holidays are observed on the next working day.
    Saturday holidays are NOT observed/replaced.
    Returns a dict of Date -> Holiday object (including observed ones).
    """
    # Convert input dict to Holiday objects
    final_holidays: Dict[dt.date, Holiday] = {}
    
    # Sort original holidays
    sorted_dates = sorted(holidays_map.keys())
    
    # First pass: Add all original holidays
    current_occupied = set(holidays_map.keys())
    
    for d in sorted_dates:
        name = holidays_map[d]
        final_holidays[d] = Holiday(date=d, name=name, is_observed=False, source="fetched")
        
        # Check for observation rule (Sunday only)
        if d.weekday() == 6:  # Sunday
            next_day = d + dt.timedelta(days=1)
            # Find next available day that is NOT currently occupied by another holiday
            # Note: We don't check for weekends here, just other holidays, 
            # because an observed holiday CAN fall on a Saturday? 
            # Actually, observed holidays usually fall on Monday. 
            # If Monday is also a holiday, it goes to Tuesday.
            while next_day in current_occupied:
                next_day += dt.timedelta(days=1)
            
            # Add observed
            obs_name = f"{name} (Observed)"
            final_holidays[next_day] = Holiday(date=next_day, name=obs_name, is_observed=True, source="rule")
            current_occupied.add(next_day)
            
    return final_holidays

def calculate_period(
    year: int, 
    month: int, 
    grade: str, 
    holidays_map: Dict[dt.date, str], 
    leave_dates: Set[dt.date]
) -> CalculationResult:
    
    # 1. Get all days
    all_days = get_days_in_month(year, month)
    
    # 2. Process holidays (apply observation rules)
    # We apply rules to the whole year context usually, but here we might only have month data?
    # Ideally holidays_map should cover at least this month + overlapping range.
    # For now, we assume holidays_map is sufficient.
    processed_holidays = apply_observed_rule(holidays_map)
    
    # Filter holidays to this month only
    month_holidays = [h for d, h in processed_holidays.items() if d.year == year and d.month == month]
    month_holiday_dates = {h.date for h in month_holidays}
    
    working_days = []
    applied_leave = []
    ignored_leave = []
    weekend_count = 0
    
    for day in all_days:
        # Check weekend
        if is_weekend(day):
            weekend_count += 1
            continue
            
        # Check holiday
        if day in month_holiday_dates:
            continue
            
        # Check leave (Personal leave only counts on working days)
        if day in leave_dates:
            applied_leave.append(day)
            continue
            
        # It's a working day
        working_days.append(day)
        
    # Check for leave dates that were ignored (e.g. on weekends or holidays or outside month)
    # Ignored leave = all leave dates provided - applied leave
    # But we only care about dates IN this month for the report explanation
    for ld in leave_dates:
        if ld.year == year and ld.month == month:
            if ld not in applied_leave:
                ignored_leave.append(ld)

    rate = GRADE_RATES.get(grade, 0)
    
    return CalculationResult(
        grade=grade,
        rate=rate,
        year=year,
        month=month,
        total_days_in_month=len(all_days),
        working_days_count=len(working_days),
        weekend_days_count=weekend_count,
        public_holidays_count=len(month_holidays),
        personal_leave_count=len(applied_leave),
        holidays=sorted(month_holidays, key=lambda h: h.date),
        working_days=working_days,
        leave_days=sorted(applied_leave),
        ignored_leave_dates=sorted(ignored_leave),
        total_reimbursement=len(working_days) * rate
    )
