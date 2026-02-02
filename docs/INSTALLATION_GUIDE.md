# QSB TLRS Calculator - Installation Guide

## Overview

The QSB TLRS Calculator now supports two distribution methods:
1. **Installed Version** - Installs to `%LOCALAPPDATA%` with Start Menu shortcuts
2. **Portable Version** - Run from any folder without installation

Both versions support auto-updates without requiring admin rights!

## Why This Approach?

✅ **No Admin Rights Required** - Installs to user space (`%LOCALAPPDATA%`)  
✅ **Seamless Auto-Updates** - Updates work without UAC prompts  
✅ **Professional Experience** - Start Menu shortcuts, proper uninstaller  
✅ **Flexible** - Users can choose installed or portable  

---

## For End Users

### Option 1: Installed Version (Recommended)

1. **Download** the `installer_package` folder
2. **Install winshell** (one-time requirement):
   ```cmd
   pip install winshell
   ```
3. **Run the installer**:
   ```cmd
   cd installer_package
   python installer.py
   ```
4. **Follow the prompts**:
   - Choose whether to create Desktop shortcut
   - Application will be installed to `%LOCALAPPDATA%\QSB_TLRS\`
   - Start Menu shortcut will be created

5. **Launch** from Start Menu: Search for "QSB TLRS Calculator"

### Option 2: Portable Version

1. **Download** the `portable_version` folder
2. **Run** `tlrs.exe` directly
3. No installation needed - works from any location

### Uninstalling (Installed Version)

Run the uninstaller:
```cmd
python "%LOCALAPPDATA%\QSB_TLRS\uninstall.py"
```

Or manually:
- Delete `%LOCALAPPDATA%\QSB_TLRS\` folder
- Delete Start Menu shortcut
- Delete Desktop shortcut (if created)

---

## For Developers

### Building the Application

1. **Install dependencies**:
   ```cmd
   pip install pyinstaller openpyxl winshell
   ```

2. **Run the build script**:
   ```cmd
   python build_installer.py
   ```

3. **Output**:
   - `installer_package/` - Contains installer and executable
   - `portable_version/` - Contains portable executable
   - `dist/` - Raw PyInstaller output

### Build Process Details

The `build_installer.py` script:
1. Checks all dependencies are installed
2. Runs PyInstaller with `tlrs.spec`
3. Creates installer package with:
   - `tlrs.exe` (main executable)
   - `qsb_tlrs.ico` (application icon)
   - `installer.py` (installation script)
   - `README.txt` (user instructions)
4. Creates portable package with just the executable

### Manual Build (Alternative)

If you prefer manual steps:

```cmd
# Build executable
pyinstaller tlrs.spec

# Create installer package manually
mkdir installer_package
copy dist\tlrs.exe installer_package\
copy qsb_tlrs.ico installer_package\
copy installer.py installer_package\
```

---

## For IT Departments

### Deployment Options

#### Option A: User Self-Install (Recommended)
1. Share the `installer_package` folder via network drive or email
2. Users run `python installer.py`
3. No admin rights required
4. Each user gets their own installation

#### Option B: Pre-Install Script
Create a deployment script that runs `installer.py` silently:

```python
# deploy.py
import subprocess
import sys

# Run installer with default options
result = subprocess.run([sys.executable, "installer.py"], 
                       input="n\ny\n",  # No desktop, yes launch
                       text=True)
```

#### Option C: Portable Deployment
Simply copy `portable_version/tlrs.exe` to a shared network location.
Users can run it directly or copy to their local machine.

### Group Policy Considerations

Since the app installs to `%LOCALAPPDATA%`:
- ✅ No admin rights needed
- ✅ Works with standard user accounts
- ✅ Each user has independent settings
- ✅ Auto-updates work without IT intervention
- ❌ Cannot use MSI deployment via GPO (use Option A or B instead)

### Network Locations

The installer works with:
- Local drives (C:, D:, etc.)
- Network drives (\\server\share)
- User profile locations (%USERPROFILE%, %LOCALAPPDATA%)

---

## Auto-Update Configuration

### For Developers

1. **Configure SharePoint URL** in `updater.py`:
   ```python
   VERSION_JSON_URL = "https://your-sharepoint-url/version.json"
   ```

2. **Create `version.json`** on SharePoint:
   ```json
   {
       "version": "1.0.1",
       "download_url": "https://your-sharepoint-url/tlrs.exe",
       "release_notes": "Bug fixes and improvements",
       "published_at": "2026-01-22"
   }
   ```

3. **Upload new versions**:
   - Build new executable
   - Upload to SharePoint
   - Update `version.json` with new version number and URL

### For End Users

Auto-updates work automatically:
- App checks for updates on startup
- Downloads update in background
- Prompts user to install
- No admin rights required
- Works for both installed and portable versions

---

## Installation Locations

### Installed Version
- **Executable**: `%LOCALAPPDATA%\QSB_TLRS\tlrs.exe`
- **Settings**: `%LOCALAPPDATA%\QSB_TLRS\tlrs_settings.json`
- **Holiday Cache**: `%LOCALAPPDATA%\QSB_TLRS\holiday_cache_*.json`
- **Start Menu**: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\QSB TLRS Calculator\`
- **Desktop** (optional): `%USERPROFILE%\Desktop\QSB TLRS Calculator.lnk`

### Portable Version
All files stored in the same folder as `tlrs.exe`:
- `tlrs.exe`
- `tlrs_settings.json`
- `holiday_cache_*.json`

---

## Troubleshooting

### "winshell module not found"
```cmd
pip install winshell
```

### "Cannot create shortcut"
- Check if Start Menu folder is accessible
- Try running as different user
- Use portable version as alternative

### "Update failed - Access denied"
- Should not happen with `%LOCALAPPDATA%` installation
- If it does, check folder permissions
- Try portable version

### "Python not found"
- Install Python from python.org
- Or use pre-built executable (no Python needed)

---

## Comparison: Installed vs Portable

| Feature | Installed | Portable |
|---------|-----------|----------|
| Start Menu shortcut | ✅ Yes | ❌ No |
| Desktop shortcut | ✅ Optional | ❌ No |
| Uninstaller | ✅ Yes | ❌ Manual |
| Auto-updates | ✅ Yes | ✅ Yes |
| Admin rights | ❌ Not needed | ❌ Not needed |
| Run from USB | ❌ No | ✅ Yes |
| Multiple users | ✅ Separate installs | ✅ Shared exe |

---

## Next Steps

1. **Test the installer** on a clean machine
2. **Configure SharePoint** for auto-updates
3. **Distribute** to users via preferred method
4. **Monitor** update adoption

For questions or issues, contact IT support.
