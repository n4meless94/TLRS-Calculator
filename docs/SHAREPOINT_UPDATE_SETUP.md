# SharePoint/OneDrive Auto-Update Setup Guide

## Overview
The application checks SharePoint/OneDrive for updates. Staff don't need any special accounts - they just use their existing Microsoft 365 access.

---

## Setup Steps

### Step 1: Create SharePoint Folder

1. Go to your SharePoint site (e.g., `https://qsb.sharepoint.com/sites/IT`)
2. Create a folder: `Shared Documents/TLRS` (or any location)
3. This folder will contain:
   - `version.json` - Version information
   - `QSB_TLRS_Calculator.exe` - Latest executable

### Step 2: Upload Files

Upload these two files to your SharePoint folder:

**File 1: `version.json`**
```json
{
    "version": "1.0.0",
    "download_url": "https://your-sharepoint-url/QSB_TLRS_Calculator.exe",
    "release_notes": "Initial release\n- Grade-based calculation\n- Holiday fetching\n- Excel export",
    "published_at": "2026-01-22"
}
```

**File 2: `QSB_TLRS_Calculator.exe`**
- Upload the compiled executable

### Step 3: Get Direct Download Links

For each file, get the direct download link:

1. Right-click the file in SharePoint
2. Click "Copy link" or "Share"
3. Click "Copy direct link" (important!)
4. The URL should look like:
   ```
   https://qsb.sharepoint.com/:u:/s/IT/EabcdefGHIJKLMNOP...
   ```

**Alternative method:**
1. Click the file
2. Click the "..." menu → Details
3. Copy the "Path" URL
4. Add `?download=1` at the end

### Step 4: Configure updater.py

Edit `updater.py` line 18:

```python
VERSION_JSON_URL = "https://your-sharepoint-direct-link/version.json"
```

**Example:**
```python
VERSION_JSON_URL = "https://qsb.sharepoint.com/:u:/s/IT/EabcdefGHIJKLMNOP/version.json?download=1"
```

### Step 5: Test the Configuration

Run the test:
```cmd
python updater.py
```

Should output:
```
Testing SharePoint/OneDrive updater...
Latest release found:
  Version: 1.0.0
  Download URL: https://...
```

### Step 6: Build Final Executable

```cmd
pyinstaller tlrs.spec
```

---

## Releasing Updates

### When you have a new version:

1. **Update version** in `settings.py`:
   ```python
   APP_VERSION = "1.0.1"
   ```

2. **Rebuild executable**:
   ```cmd
   pyinstaller tlrs.spec
   ```

3. **Upload to SharePoint**:
   - Upload new `QSB_TLRS_Calculator.exe` (replace old one)
   - Update `version.json`:
     ```json
     {
         "version": "1.0.1",
         "download_url": "https://your-sharepoint-url/QSB_TLRS_Calculator.exe",
         "release_notes": "Bug fixes:\n- Fixed leave date persistence\n- Improved window sizing",
         "published_at": "2026-01-23"
     }
     ```

4. **Done!** Users will see update notification on next app start

---

## SharePoint Permissions

### Who needs access?

**Only you (IT admin):**
- Edit permission to upload files
- Manage the SharePoint folder

**Staff (end users):**
- Read permission (usually automatic for company SharePoint)
- No special setup needed
- They use their existing Microsoft 365 login

### Setting Permissions:

1. Go to SharePoint folder
2. Click "Share" or "Manage access"
3. Options:
   - **"Anyone in organization"** - All QSB staff can access (recommended)
   - **"Specific people"** - Only selected staff
   - **"People with existing access"** - Inherit from parent folder

---

## OneDrive Alternative

If using OneDrive instead of SharePoint:

1. Create folder in your OneDrive: `TLRS Updates`
2. Upload `version.json` and exe
3. Right-click → Share → "Anyone with the link"
4. Copy the link
5. Convert to direct download:
   - Change `redir` to `download` in URL
   - Or add `&download=1` at the end

**Example:**
```
Original: https://onedrive.live.com/redir?resid=ABC123
Direct:   https://onedrive.live.com/download?resid=ABC123
```

---

## version.json Format

```json
{
    "version": "1.0.1",
    "download_url": "https://direct-link-to-exe",
    "release_notes": "What's new in this version",
    "published_at": "2026-01-22"
}
```

**Fields:**
- `version` (required): Version number (e.g., "1.0.1")
- `download_url` (required): Direct download link to exe
- `release_notes` (optional): What's new (use `\n` for line breaks)
- `published_at` (optional): Release date

---

## Troubleshooting

### "No release found or error occurred"
- Check VERSION_JSON_URL is correct
- Ensure version.json is accessible (test in browser)
- Verify JSON format is valid (use jsonlint.com)

### "Download failed"
- Check download_url in version.json
- Ensure exe file is accessible
- Try the URL in browser - should download file

### "Access denied"
- Check SharePoint permissions
- Ensure "Anyone in organization" can read
- Staff might need to sign in to Microsoft 365

### Update doesn't trigger
- Check "Check for updates on startup" is enabled in Settings
- Verify current version is lower than server version
- Check internet connection

---

## Security Notes

1. **SharePoint is secure** - Only QSB staff with Microsoft 365 can access
2. **No passwords in code** - Uses existing Microsoft authentication
3. **Internal only** - Files not accessible outside organization
4. **Audit trail** - SharePoint tracks who accessed files

---

## Advantages of SharePoint/OneDrive

✅ No GitHub account needed
✅ Staff already have access (Microsoft 365)
✅ Easy to manage (just upload files)
✅ Secure (company authentication)
✅ Audit trail built-in
✅ Works with existing infrastructure

---

## Quick Reference

**To release update:**
1. Change version in `settings.py`
2. Build: `pyinstaller tlrs.spec`
3. Upload exe to SharePoint
4. Update `version.json` with new version number
5. Done!

**Files needed in SharePoint:**
- `version.json` - Version info
- `QSB_TLRS_Calculator.exe` - Latest executable

**Staff experience:**
- App checks for updates on startup
- Shows notification if update available
- One-click download & install
- No login or account needed
