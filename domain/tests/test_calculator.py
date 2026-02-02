
import unittest
from datetime import date
from domain.calculator import calculate_period, apply_observed_rule, is_weekend, get_days_in_month

class TestCalculator(unittest.TestCase):
    
    def test_is_weekend(self):
        # 2026-02-01 is Sunday
        self.assertTrue(is_weekend(date(2026, 2, 1)))
        # 2026-02-02 is Monday
        self.assertFalse(is_weekend(date(2026, 2, 2)))
        # 2026-02-07 is Saturday
        self.assertTrue(is_weekend(date(2026, 2, 7)))

    def test_sunday_observation_rule(self):
        # Case: Holiday on Sunday (2026-02-01)
        # Should create an observed holiday on Monday (2026-02-02)
        holidays_map = {
            date(2026, 2, 1): "Test Holiday"
        }
        final = apply_observed_rule(holidays_map)
        
        self.assertIn(date(2026, 2, 1), final)
        self.assertIn(date(2026, 2, 2), final)
        self.assertTrue(final[date(2026, 2, 2)].is_observed)
        self.assertEqual(final[date(2026, 2, 2)].name, "Test Holiday (Observed)")

    def test_sunday_observation_chained(self):
        # Case: Holiday on Sunday AND Monday
        # Sunday (1st) -> Observes on Monday (2nd) -> Monday is occupied -> Observes on Tuesday (3rd)
        # Wait, if Monday is ALSO a holiday, then:
        # 1. Sunday's replacement looks for next available. Monday is occupied by Holiday B. So it goes to Tuesday.
        # 2. Monday (Holiday B) stays on Monday.
        
        holidays_map = {
            date(2026, 2, 1): "Holiday A",  # Sun
            date(2026, 2, 2): "Holiday B"   # Mon
        }
        
        final = apply_observed_rule(holidays_map)
        
        # Original holidays present
        self.assertIn(date(2026, 2, 1), final)
        self.assertIn(date(2026, 2, 2), final)
        
        # Holiday A (Sun) should drift to Tuesday (3rd) because Monday (2nd) is occupied
        # Let's trace my code logic:
        # sort: 1st, 2nd
        # Process 1st (Sun): next=2nd. 2nd in current_occupied? Yes (Holiday B). next=3rd.
        # Add 3rd.
        # Process 2nd (Mon): Not Sun. No action.
        
        self.assertIn(date(2026, 2, 3), final)
        self.assertEqual(final[date(2026, 2, 3)].name, "Holiday A (Observed)")

    def test_golden_feb_2024_leap_year(self):
        # Feb 2024: 29 days.
        # Weekends: 3,4, 10,11, 17,18, 24,25 (8 days)
        # Holidays: CNY 10 (Sat), 11 (Sun).
        # Rules: 
        #   10 (Sat): No replacement.
        #   11 (Sun): Replaced to 12 (Mon).
        # Expected Non-Working: 8 weekends + 12th = 9 days.
        # Expected Working: 29 - 9 = 20 days.
        
        holidays_map = {
            date(2024, 2, 10): "CNY Day 1",
            date(2024, 2, 11): "CNY Day 2"
        }
        leave_dates = set()
        
        result = calculate_period(2024, 2, "JG6", holidays_map, leave_dates)
        
        self.assertEqual(result.total_days_in_month, 29, "Leap year failure")
        self.assertEqual(result.public_holidays_count, 3, "Should have 2 original + 1 observed")
        # Note: public_holidays_count includes weekends if they are holidays.
        # working_days calculation excludes them.
        
        # Let's count explicitly
        # 10 (Sat) - Weekend
        # 11 (Sun) - Weekend
        # 12 (Mon) - Observed Holiday
        # Working days should exclude weekends and 12th.
        
        self.assertNotIn(date(2024, 2, 10), result.working_days)
        self.assertNotIn(date(2024, 2, 11), result.working_days)
        self.assertNotIn(date(2024, 2, 12), result.working_days)
        
        self.assertEqual(result.working_days_count, 20)
        self.assertEqual(result.total_reimbursement, 2000) # 20 * 100

    def test_leave_deduction(self):
        # March 2026
        # 1st is Sun. Weekends: 1, 7,8, 14,15, 21,22, 28,29 (9 days).
        # Total: 31.
        # Working: 22.
        # Leave: Apply on 4th (Wed) -> Should deduct 1.
        # Leave: Apply on 7th (Sat) -> Should NOT deduct (ignored).
        
        holidays_map = {}
        leave_dates = {date(2026, 3, 4), date(2026, 3, 7)}
        
        result = calculate_period(2026, 3, "JG6", holidays_map, leave_dates)
        
        self.assertEqual(result.working_days_count, 21) # 22 - 1
        self.assertEqual(result.personal_leave_count, 1)
        self.assertIn(date(2026, 3, 7), result.ignored_leave_dates)

if __name__ == '__main__':
    unittest.main()
