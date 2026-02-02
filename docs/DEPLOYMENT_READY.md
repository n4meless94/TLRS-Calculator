# ✅ QSB TLRS Calculator - Beta Release Ready

## Installation Complete!

Your application now has a professional installer that installs to `%LOCALAPPDATA%\QSB_TLRS\` with:
- ✅ Start Menu shortcuts
- ✅ Desktop shortcut (optional)
- ✅ Uninstaller
- ✅ Auto-update support (no admin rights needed)

## What You Have

### 📁 installer_package/
**For users who want proper installation**
- `QSB_TLRS_Calculator.exe` - Main application
- `installer.py` - Installation script
- `qsb_tlrs.ico` - Application icon
- `README.txt` - User instructions

**To install:**
```cmd
cd installer_package
py installer.py
```

### 📁 portable_version/
**For users who prefer portable apps**
- `QSB_TLRS_Calculator.exe` - Main application
- `qsb_tlrs.ico` - Application icon
- `README.txt` - User instructions

**To use:**
Just run `QSB_TLRS_Calculator.exe` - no installation needed!

### 📁 dist/
Raw PyInstaller output (for reference)

## Installation Locations

### Installed Version
- **Executable**: `C:\Users\[Username]\AppData\Local\QSB_TLRS\QSB_TLRS_Calculator.exe`
- **Settings**: `C:\Users\[Username]\AppData\Local\QSB_TLRS\tlrs_settings.json`
- **Holiday Cache**: `C:\Users\[Username]\AppData\Local\QSB_TLRS\holiday_cache_*.json`
- **Start Menu**: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\QSB TLRS Calculator\`
- **Desktop**: `%USERPROFILE%\Desktop\QSB TLRS Calculator.lnk` (if created)

### Portable Version
All files stay in the same folder as the executable.

## How to Distribute

### Option 1: Share installer_package folder
1. Zip the `installer_package` folder
2. Share via email, network drive, or SharePoint
3. Users extract and run `py installer.py`
4. Application installs with shortcuts

### Option 2: Share portable_version folder
1. Zip the `portable_version` folder
2. Share via email, network drive, or SharePoint
3. Users extract and run `QSB_TLRS_Calculator.exe`
4. No installation needed

### Option 3: SharePoint/OneDrive Distribution
1. Upload `installer_package` to SharePoint
2. Share the link with users
3. Users download and run installer

## Auto-Update Setup

To enable auto-updates:

1. **Configure SharePoint URL** in `updater.py`:
   ```python
   VERSION_JSON_URL = "https://your-sharepoint-url/version.json"
   ```

2. **Create version.json** on SharePoint:
   ```json
   {
       "version": "0.9.0",
       "download_url": "https://your-sharepoint-url/QSB_TLRS_Calculator.exe",
       "release_notes": "Bug fixes and improvements",
       "published_at": "2026-01-22"
   }
   ```

3. **Upload new versions**:
   - Build new executable: `py build_installer.py`
   - Upload `dist/QSB_TLRS_Calculator.exe` to SharePoint
   - Update `version.json` with new version number

4. **Users get updates automatically**:
   - App checks for updates on startup
   - Downloads in background
   - Prompts to install
   - No admin rights required!

## Uninstalling

### Installed Version
```cmd
py "%LOCALAPPDATA%\QSB_TLRS\uninstall.py"
```

Or manually:
- Delete `%LOCALAPPDATA%\QSB_TLRS\` folder
- Delete Start Menu shortcut
- Delete Desktop shortcut (if created)

### Portable Version
Just delete the folder - no traces left behind.

## Building New Versions

```cmd
# 1. Make your code changes
# 2. Update version in settings.py
# 3. Build
py build_installer.py

# Output:
# - installer_package/ (ready to distribute)
# - portable_version/ (ready to distribute)
```

## Dependencies (for building)

```cmd
py -m pip install pyinstaller openpyxl pywin32 winshell
```

## Testing Checklist

- [x] Build completes successfully
- [x] Installer creates shortcuts
- [x] Application launches from Start Menu
- [x] Application launches from Desktop shortcut
- [x] Settings persist between runs
- [x] Portable version works independently
- [ ] Auto-update works (configure SharePoint first)

## Next Steps

1. **Test the installed application** - Check all features work
2. **Configure auto-updates** - Set up SharePoint/OneDrive
3. **Distribute to pilot users** - Get feedback
4. **Roll out to all users** - Share installer_package or portable_version

## Support

For issues or questions:
- Check `INSTALLATION_GUIDE.md` for detailed documentation
- Review `AUTO_UPDATE_SETUP.md` for update configuration
- Contact IT support

---

**Built on:** January 22, 2026  
**Version:** 0.9.0 (Beta)  
**Build System:** PyInstaller + Custom Installer  
**Target:** Windows 10/11
