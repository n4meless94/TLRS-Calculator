
import unittest
import shutil
from pathlib import Path
from datetime import date
from domain.models import CalculationResult, Holiday
from exporters.excel_exporter import ExcelExporter
from exporters.csv_exporter import CsvExporter

class TestExporterIntegration(unittest.TestCase):
    """
    Integration tests for Exporters.
    Verifies interaction with FileSystem (File Creation).
    """
    def setUp(self):
        self.test_dir = Path("tests/integration_temp_exp")
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()
        
        # Dummy Result
        self.res = CalculationResult(
            grade="JG6", rate=100, year=2026, month=1,
            total_days_in_month=31, working_days_count=20, 
            weekend_days_count=8, public_holidays_count=1, personal_leave_count=2,
            working_days=[date(2026,1,2)],
            holidays=[Holiday(date(2026,1,1), "New Year")],
            total_reimbursement=2000
        )

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_excel_creation(self):
        filename = self.test_dir / "test.xlsx"
        exporter = ExcelExporter(self.res, "Integration Test")
        exporter.export(str(filename))
        
        self.assertTrue(filename.exists())
        self.assertGreater(filename.stat().st_size, 1000, "Excel file seems too small")

    def test_csv_creation(self):
        filename = self.test_dir / "test.csv"
        exporter = CsvExporter(self.res)
        exporter.export(str(filename))
        
        self.assertTrue(filename.exists())
        
        # Verify Content
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("JG6", content)
            self.assertIn("New Year", content)
