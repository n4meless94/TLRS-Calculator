# TLRS Working Day Calculator

A modern desktop application for calculating working day reimbursements with automatic holiday detection, personal leave management, and professional export capabilities.

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

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

### Export Capabilities
- **PDF Export** - Print-ready calendar with legend and holiday details
- **Excel Export** - Professional spreadsheet with:
  - Calendar sheet (monthly grid view, print-ready A4 landscape)
  - Details sheet (audit trail with all dates and statuses)
  - Summary block with grade rates and totals
  - Holiday source notes (online/offline/cached)
- **CSV Export** - Simple tabular format for further analysis

## 🚀 Quick Start

### Running the Application
1. Download the executable from [Releases](https://github.com/n4meless94/TLRS-Calculator/releases)
2. Double-click to run (no installation required)
3. Select your grade
4. Choose month and year
5. (Optional) Enter personal leave dates
6. Click "Calculate"
7. Export as PDF, Excel, or CSV as needed

### Building from Source

```bash
# Clone the repository
git clone https://github.com/n4meless94/TLRS-Calculator.git
cd TLRS-Calculator

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
- **Developer Mode**: Show debug logs tab for troubleshooting

### Holiday Data Source
The application fetches public holidays from a configurable source. By default, it uses online holiday APIs with local caching for offline use.

## 🏗️ Architecture

```
main.py                   # Application entry point
domain/
  ├── calculator.py       # Core calculation engine
  └── models.py           # Data models
services/
  ├── holiday_service.py  # Holiday fetching & caching
  └── settings_service.py # Settings persistence
exporters/
  ├── pdf_exporter.py     # PDF generation
  ├── excel_exporter.py   # Excel generation
  └── csv_exporter.py     # CSV generation
ui/
  ├── main_window.py      # Main application window
  ├── styles.py           # UI theme and constants
  └── components/         # Reusable UI widgets
tests/
  ├── domain/            # Unit tests
  ├── integration/       # Integration tests
  └── acceptance/        # End-to-end tests
```

## 🔧 Technical Stack

- **GUI**: Python Tkinter/TTK
- **PDF**: ReportLab + PyMuPDF
- **Excel**: OpenPyXL
- **Packaging**: PyInstaller (single-file executable)
- **Testing**: Pytest

## 📋 Requirements

- **Python**: 3.8+
- **OS**: Windows 10/11 (for executable; source code is cross-platform)
- **Internet**: Required for initial holiday download
- **Disk**: ~50MB free space

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

Contributions are welcome! Please feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Support

For issues or feature requests, please [open an issue](https://github.com/n4meless94/TLRS-Calculator/issues) on GitHub.

---

**Made with ❤️ for efficient working day calculations**
