# Installation Guide

## For End Users (Using the Executable)

1. Download `tlrs.exe` from the `dist/` folder
2. Double-click to run - no installation needed!
3. The Excel export feature is built-in

## For Developers (Running from Source)

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or download the repository**

2. **Install required packages**
   ```cmd
   pip install openpyxl
   ```

3. **Run the application**
   ```cmd
   python tlrs_gui_v2.py
   ```

### Building the Executable

If you want to build the executable yourself:

1. **Install PyInstaller**
   ```cmd
   pip install pyinstaller
   ```

2. **Build the executable**
   ```cmd
   pyinstaller tlrs.spec
   ```

3. **Find the executable**
   - The built executable will be in the `dist/` folder
   - File name: `tlrs.exe`

## Features Requiring openpyxl

The Excel export feature requires the `openpyxl` library. If you're running from source and haven't installed it:

```cmd
pip install openpyxl
```

Without openpyxl:
- ✅ All calculation features work
- ✅ CSV export works
- ✅ Copy to clipboard works
- ❌ Excel export button will show an error

## Troubleshooting

### "openpyxl not found" error
```cmd
pip install openpyxl
```

### Python not found
- Download Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### Permission errors on Windows
- Run Command Prompt as Administrator
- Or install packages with `--user` flag:
  ```cmd
  pip install --user openpyxl
  ```

## System Requirements

- **Operating System**: Windows 7 or higher
- **RAM**: 512 MB minimum
- **Disk Space**: 50 MB for executable, 200 MB for Python + dependencies
- **Internet**: Required for fetching Sabah public holidays (optional - can use offline mode)
