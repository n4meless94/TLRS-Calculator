
import unittest
import shutil
import json
import threading
from pathlib import Path
from datetime import date
from services.holiday_service import HolidayService

class TestServiceIntegration(unittest.TestCase):
    """
    Integration tests for HolidayService.
    Verifies interaction with FileSystem (Cache).
    """
    
    def setUp(self):
        self.test_dir = Path("tests/integration_temp")
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()
        self.service = HolidayService(str(self.test_dir))

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_cache_roundtrip(self):
        """Verify we can save to disk and reload correctly."""
        year = 2099
        data = {date(2099, 1, 1): "Future Day"}
        
        # 1. Save
        self.service.save_to_cache(year, data)
        
        # 2. Check File
        expected_file = self.test_dir / f"holiday_cache_{year}.json"
        self.assertTrue(expected_file.exists())
        
        # 3. Load
        loaded_data = self.service.load_from_cache(year)
        self.assertIsNotNone(loaded_data)
        self.assertEqual(loaded_data["year"], year)
        self.assertIn("2099-01-01", loaded_data["holidays"])
        self.assertEqual(loaded_data["holidays"]["2099-01-01"], "Future Day")

    def test_async_fetch_simulation(self):
        """Verify threading mechanism works with callbacks."""
        # Note: We won't hit the real network, but we'll mock the internal fetch
        # to ensure the threading/queueing part works.
        
        # Monkey patch the sync fetcher to return immediate data
        self.service.fetch_holidays_sync = lambda year: {date(year, 1, 1): "Mock Holiday"}
        
        result_container = {}
        event = threading.Event()
        
        def on_success(holidays, source):
            result_container['data'] = holidays
            result_container['source'] = source
            event.set()
            
        def on_error(msg):
            result_container['error'] = msg
            event.set()
            
        # Call async
        self.service.fetch_holidays_async(2030, on_success, on_error, force_refresh=True)
        
        # Wait
        success = event.wait(timeout=2.0)
        self.assertTrue(success, "Async callback timed out")
        self.assertIn(date(2030, 1, 1), result_container.get('data', {}))
        self.assertEqual(result_container['source'], "Live Fetch")
