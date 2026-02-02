# Project Structure

```
├── tlrs.py              # Core calculation logic (CLI version)
├── tlrs_gui.py          # Legacy GUI (v1)
├── tlrs_gui_v2.py       # Modern GUI application (main entry point)
├── settings.py          # Settings management, app constants, persistence
├── excel_export.py      # CalendarExporter class for Excel output
├── tlrs.spec            # PyInstaller build configuration
├── qsb_tlrs.ico         # Application icon
├── dist/                # Built executable output
│   └── tlrs.exe
├── build/               # PyInstaller build artifacts
├── holiday_cache_*.json # Cached holiday data per year
└── tlrs_settings.json   # User settings (auto-generated)
```

## Module Responsibilities

### tlrs.py
- `GRADE_RATES` - Grade to rate mapping
- `fetch_holidays()` / `fetch_holidays_with_names()` - Scrape sabah.gov.my
- `apply_sunday_observed_rule()` - Holiday observation logic
- `working_days()` - Calculate eligible days
- `calculate_reimbursement()` - Compute total amount
- `parse_date()` / `parse_dates()` - Multi-format date parsing

### tlrs_gui_v2.py
- `TLRSAppV2` - Main application class
- `HolidayCache` - File-based holiday caching
- `CalculationResult` - View model for results

### settings.py
- `SettingsManager` - JSON-based settings persistence
- App metadata constants (version, organization, disclaimer)
- `DEFAULT_GRADE_RATES` - Rate configuration

### excel_export.py
- `CalendarExporter` - Two-sheet Excel workbook generation
- Calendar sheet: Monthly grid view (Monday-first)
- Details sheet: Tabular breakdown with status
