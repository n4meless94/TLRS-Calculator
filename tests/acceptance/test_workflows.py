
import unittest
from datetime import date
from domain.calculator import calculate_period
from domain.models import CalculationResult, Holiday

class TestAcceptanceWorkflows(unittest.TestCase):
    """
    End-to-End Acceptance Tests / Story Tests.
    Simulates high-level user goals independent of UI.
    """
    
    def test_story_regular_claim(self):
        """
        Story: User claims for March 2026 (JG6).
        Assumption: No unexpected holidays beyond cache.
        Goal: Verify eligible days and amount match business expectation.
        """
        # 1. Setup Context
        year = 2026
        month = 3
        grade = "JG6" # RM 100/day
        
        # 2. External Data (Mocked from "Service")
        # March 2026: 
        # 1st (Sun), 7,8, 14,15, 21,22, 28,29 (Weekends)
        # 23 Mar (Tue), 24 Mar (Wed) = Hari Raya Aidilfitri
        holidays_map = {
            date(2026, 3, 23): "Hari Raya Aidilfitri",
            date(2026, 3, 24): "Hari Raya Aidilfitri Day 2"
        }
        
        # 3. User Input (Leave)
        # Took leave on 25th (Thu) and 26th (Fri)
        leave_dates = {date(2026, 3, 25), date(2026, 3, 26)}
        
        # 4. Action (Click Calculate)
        result = calculate_period(year, month, grade, holidays_map, leave_dates)
        
        # 5. Assertions (The "Receipt")
        
        # Total Calendar Days: 31
        self.assertEqual(result.total_days_in_month, 31)
        
        # Weekends: 1, 7,8, 14,15, 21,22, 28,29 = 9 days
        self.assertEqual(result.weekend_days_count, 9)
        
        # Holidays: 23, 24 = 2 days
        self.assertEqual(result.public_holidays_count, 2)
        
        # Personal Leave: 25, 26 = 2 days
        self.assertEqual(result.personal_leave_count, 2)
        
        # Working: 31 - 9 - 2 - 2 = 18 days
        self.assertEqual(result.working_days_count, 18)
        
        # Money: 18 * 100 = 1800
        self.assertEqual(result.total_reimbursement, 1800)
        
    def test_story_offline_mode_with_weekend_holiday(self):
        """
        Story: User runs offline, ignores Sabah holidays, but manually adds one that falls on Sunday.
        Goal: Verify logic handles Sunday observation even with manual input.
        """
        # User input manual holiday: 1st Feb 2026 (Sunday) - Federal Territory Day
        holidays_map = {date(2026, 2, 1): "FT Day"}
        
        result = calculate_period(2026, 2, "JG5", holidays_map, set())
        
        # 1st (Sun) is Holiday.
        # Should be Observed on 2nd (Mon).
        
        # Weekends in Feb 2026: 1, 7,8, 14,15, 21,22, 28 = 8 days.
        # Holidays count: 1 (Original) + 1 (Observed)?
        # Our model counts distinct holiday objects in list.
        # 1st is holiday AND weekend.
        # 2nd is observed holiday (non-working).
        
        # So Working days should exclude:
        # - All weekends (incl 1st)
        # - The observed day (2nd)
        
        # Total 28 days.
        # Weekends: 8.
        # Additional non-working (2nd): 1.
        # Working: 28 - 9 = 19.
        
        self.assertEqual(result.working_days_count, 19)
        # Check that 2nd Feb is indeed flagged as observed
        observed = [h for h in result.holidays if h.is_observed]
        self.assertEqual(len(observed), 1)
        self.assertEqual(observed[0].date, date(2026, 2, 2))
        
