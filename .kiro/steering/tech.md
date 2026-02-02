# Tech Stack

## Language
- Python 3.7+

## GUI Framework
- tkinter (standard library)
- ttk for themed widgets

## Dependencies
- `openpyxl` - Excel file generation with formatting
- Standard library: `calendar`, `datetime`, `json`, `csv`, `urllib`, `threading`

## Build System
- PyInstaller for Windows executable packaging

## Common Commands

### Run Application
```cmd
python tlrs_gui_v2.py
```

### Run CLI Version
```cmd
python tlrs.py --grade JG5 --year 2026 --month 3
python tlrs.py --grade JG8 --year 2026 --month 3 --leave 2026-03-12,2026-03-15
```

### Install Dependencies
```cmd
pip install openpyxl
```

### Build Executable
```cmd
pip install pyinstaller
pyinstaller tlrs.spec
```
Output: `dist/tlrs.exe`

## Code Style
- Type hints used throughout
- Docstrings for modules and classes
- Constants in UPPER_CASE
- Classes use PascalCase
- Functions/variables use snake_case
