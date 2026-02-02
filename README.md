# TLRS Working Day Calculator

A modern desktop application for calculating working day reimbursements with automatic holiday detection, personal leave management, and professional export capabilities.

## ✨ Features

### Smart Calculation Engine
- **Automatic working day calculation** excluding weekends and public holidays
- **Holiday detection** with configurable regional support
- **Sunday-observed holiday rule** (holidays falling on Sunday are observed on the next weekday)
- **Personal leave exclusion** with flexible date input
- **Grade-based reimbursement rates** (customizable)

### Modern User Interface
- **Clean two-column layout** with visual hierarchy
- **Live PDF preview** with month navigation arrows (◄ ►)
- **Period navigation** with Previous/Next buttons and Today shortcut
- **Settings tab** for default grade, auto-open exports, and cache management
- **Developer mode** with optional debug logs
- **Smart leave input** with validation and duplicate detection
- **Offline mode** for calculations without internet
- **Holiday caching** to reduce network requests

### Results Display
- **Summary cards** showing:
  - Working days, weekends, holidays, and leave counts
  - Total reimbursement calculation
- **Interactive calendar view** with color-coded day types
- **Detailed breakdowns** in tabbed interface
- **Modern confirmation dialogs** with flat design

### Export & Documentation
- **PDF Export** - Print-ready calendar with legend and holiday details
- **Excel Export** - Professional spreadsheet with:
  - Calendar sheet (monthly grid view, print-ready A4 landscape)
  - Details sheet (audit trail with all dates and statuses)
  - Summary block with grade rates and totals
  - Holiday source notes (online/offline/cached)
- **CSV Export** - Simple tabular format for further analysis

## 🚀 Quick Start

### Running the Application
1. Download the executable from the releases
2. Double-click to run (no installation required)
3. Select your grade
4. Choose month and year
5. (Optional) Enter personal leave dates
6. Click "Calculate"
7. Export as PDF, Excel, or CSV as needed

### Building from Source

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py

# Build executable
python scripts/build_exe.py
```

The executable will be created in the `dist/` folder.

## 🗓️ Leave Date Input

Enter dates in any of these formats:
- `2026-03-12` (ISO format, recommended)
- `12-03-2026`
- `12/03/2026`
- `12 March 2026`
- `12 Mar 2026`

Multiple dates can be:
- One per line
- Comma-separated
- Mixed format (will be normalized)

Use the **Normalize** button to sort, deduplicate, and format dates to ISO standard.

## ⚙️ Configuration

### Settings Tab
- **Default Grade**: Set your preferred grade to load on startup
- **Auto-Open Export**: Automatically open PDF/Excel files after saving
- **Clear Holiday Cache**: Reset cached holiday data
- **Developer Mode**: Show debug logs tab

### Holiday Data Source
The application fetches public holidays from a configurable source. By default, it uses online holiday APIs with local caching for offline use.

## 🏗️ Architecture

```
main.py                  # Entry point
domain/
  ├── calculator.py      # Core calculation engine
  └── models.py          # Data models
services/
  ├── holiday_service.py # Holiday fetching & caching
  └── settings_service.py# Settings persistence
exporters/
  ├── pdf_exporter.py    # PDF generation
  ├── excel_exporter.py  # Excel generation
  └── csv_exporter.py    # CSV generation
ui/
  ├── main_window.py     # Main application window
  ├── styles.py          # UI theme and constants
  └── components/        # Reusable UI widgets
tests/
  ├── domain/           # Unit tests
  ├── integration/      # Integration tests
  └── acceptance/       # End-to-end tests
```

## 🔧 Technical Stack

- **GUI**: Python Tkinter/TTK
- **PDF**: ReportLab + PyMuPDF
- **Excel**: OpenPyXL
- **Packaging**: PyInstaller (single-file executable)
- **Testing**: Pytest

## 📋 Requirements

- Python 3.8+
- Windows 10/11 (for executable)
- Internet connection (for initial holiday download)

## 🐛 Known Limitations

- Year range: 2020-2030
- Executable is Windows-only (source code is cross-platform)
- Holiday source configuration requires code modification

## 📝 Version History

### v1.0 (February 2026)
- ✅ Modern UI with PDF preview navigation
- ✅ Settings tab with persistent preferences
- ✅ Developer mode for debug logs
- ✅ Two-pass border rendering for clean PDF exports
- ✅ Month navigation arrows in PDF preview
- ✅ Complete holiday border rendering
- ✅ Professional export suite (PDF, Excel, CSV)
- ✅ Comprehensive test coverage

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💬 Support

For issues or feature requests, please open an issue on GitHub.


## Features

### Calculation
- Automatic working day calculation excluding weekends and public holidays
- Sabah public holiday fetching from sabah.gov.my
- Sunday-observed holiday rule (holidays on Sunday observed next weekday)
- Personal leave exclusion support
- Grade-based reimbursement rates (JG5-JGA)

### User Interface
- **Modern two-column layout** with clear visual hierarchy
- **Grade selection** with live rate display badge
- **Period navigation** with Previous/Next month quick buttons
- **Smart leave input** with validation, normalization, and duplicate detection
- **Offline mode** for calculations without internet
- **Holiday caching** to reduce network requests and improve reliability

### Results Display
- **Summary card** showing:
  - Grade and rate
  - Period details
  - Calendar days, weekends, holidays, leave counts
  - Working days eligible
  - Total reimbursement amount
- **Tabbed details** for:
  - Public holidays (excluded)
  - Personal leave (excluded)
  - Working days (eligible)
  - Warnings and ignored items

### Export & Copy
- **Copy Summary** - Copy calculation summary to clipboard
- **Export CSV** - Export detailed breakdown for claim documentation
- **Export Excel** - Export to Excel with two sheets:
  - **Calendar Sheet** (primary, print-ready):
    - True monthly calendar grid (Sunday–Saturday layout)
    - A4 landscape, fits on 1 page
    - Large month/year title with dark blue background
    - Day-by-day status markers with minimal visual noise:
      - `WD` = Working Day (eligible, small grey text)
      - `WE` = Weekend (excluded, shown in light blue columns)
      - `PH` = Public Holiday (excluded, with holiday name in red)
      - `PL` = Personal Leave (excluded, shown in pale yellow)
    - Legend box (top-right) explaining all status markers
    - Weekend columns (Sunday/Saturday) shaded light blue
    - Out-of-month cells shaded light grey
    - Clean summary block showing:
      - Eligible working days count
      - Exclusion breakdown (weekends, holidays, leave)
      - Selected grade and daily rate
      - Total reimbursement (bold, prominent)
      - Reference table with all grade totals (selected grade highlighted)
      - Holiday source note (online/offline/cached)
    - Thin borders, no gridlines, professional appearance
    - Footer with generation timestamp
  - **Details Sheet** (secondary, for audit trail):
    - Traditional table format with all dates and statuses
    - Offline mode warning banner (if applicable)
    - Useful for verification and record-keeping
- **Refresh Holidays** - Clear cache and fetch fresh holiday data

## Grade Rates

| Grade | Rate per Day |
|-------|--------------|
| JG5   | RM50         |
| JG6   | RM100        |
| JG7   | RM150        |
| JG8   | RM200        |
| JGB   | RM200        |
| JGA   | RM250        |

## Usage

### GUI Application
1. Double-click `dist/tlrs.exe`
2. Select your grade
3. Choose month and year
4. (Optional) Enter personal leave dates
5. Click "Calculate Reimbursement"
6. View results and export as needed

### Command Line (Original)
```cmd
python tlrs.py --grade JG5 --year 2026 --month 3
python tlrs.py --grade JG8 --year 2026 --month 3 --leave 2026-03-12,2026-03-15
```

## Leave Date Input

Enter dates in any of these formats:
- `2026-03-12` (ISO format, recommended)
- `12-03-2026`
- `12/03/2026`
- `12 March 2026`
- `12 Mar 2026`

Multiple dates can be:
- One per line
- Comma-separated
- Mixed format (will be normalized)

Use the **Normalize** button to sort, deduplicate, and format dates to ISO standard.

## Validation

The calculator validates:
- Grade selection (required)
- Year range (2000-2100)
- Leave date formats
- Leave dates within selected period

Invalid dates are flagged with warnings. Dates outside the selected period are ignored and listed in the Warnings tab.

## Holiday Caching

Fetched holidays are cached locally in `holiday_cache_{year}.json` files to:
- Reduce network requests
- Improve reliability
- Speed up repeated calculations

Use **Refresh Holidays** button to clear cache and fetch fresh data.

## Files

- `tlrs.py` - Core calculation logic (CLI version)
- `tlrs_gui_v2.py` - Modern GUI application
- `tlrs.spec` - PyInstaller build configuration
- `dist/tlrs.exe` - Standalone executable (Windows)

## Building from Source

```cmd
py -m PyInstaller tlrs.spec
```

The executable will be created in the `dist/` folder.

## Requirements

- Python 3.7+
- tkinter (included with Python)
- openpyxl (for Excel export): `pip install openpyxl`
- No other external dependencies for core functionality

## Notes

- Holiday data is fetched from sabah.gov.my
- Offline mode disables holiday exclusion (totals may be higher)
- Weekends (Saturday/Sunday) are always excluded
- Observed holidays (Sunday holidays moved to Monday) are clearly marked
- All calculations follow Sabah public holiday rules

## Version History

### v0.9.0 (Beta)
- Redesigned Excel Calendar sheet for cleaner, audit-friendly layout
- Reduced visual noise: status markers (WD/WE/PH/PL) instead of verbose labels
- Added legend box explaining all status markers
- Improved summary block with clear exclusion breakdown
- Out-of-month cells shaded light grey for clarity
- Holiday source note (online/offline/cached) in footer
- Offline mode warning banner on Details sheet
- Professional print-ready formatting (A4 landscape, 1 page)
- Fixed holiday name caching to preserve actual names from sabah.gov.my

### v2.1
- Calendar grid view in Excel export (wall calendar style)
- Print-ready A4 landscape format (1 page)
- Two-sheet workbook: Calendar + Details
- Day-by-day status markers (WD/WE/PH/PL)
- Holiday names in red
- Weekend columns shaded
- Monthly summary with all grade reimbursements
- Selected grade highlighted
- Modern claim-ready GUI
- Validation and error handling
- Holiday names from sabah.gov.my
- Date format: dd/mm/yyyy
- Holiday caching
- Tabbed results display
- Copy to clipboard
- Period navigation buttons

### v1.0
- Basic GUI with scrolling results
- Command-line interface
- Holiday fetching from sabah.gov.my
