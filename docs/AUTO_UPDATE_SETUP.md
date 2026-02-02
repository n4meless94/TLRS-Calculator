# QSB TLRS Calculator - Auto-Update Setup Guide

## Overview
The application now supports automatic updates from a private GitHub repository. Users will be notified when new versions are available and can download/install with one click.

---

## GitHub Repository Setup

### Step 1: Create Private Repository

1. Go to GitHub: https://github.com
2. Click "New repository"
3. Repository settings:
   - **Name**: `tlrs-calculator` (or your preferred name)
   - **Visibility**: ✅ **Private** (important!)
   - **Description**: QSB TLRS Calculator - Internal Distribution
   - Do NOT initialize with README (optional)
4. Click "Create repository"

### Step 2: Add Team Members

1. Go to repository Settings → Collaborators
2. Add QSB team members who need access
3. They will receive email invitations

### Step 3: Configure updater.py

Edit `updater.py` and update these lines:

```python
# Line 18-19: Update with your repository info
GITHUB_REPO_OWNER = "your-github-username"  # Your GitHub username or organization
GITHUB_REPO_NAME = "tlrs-calculator"        # Your repository name
```

**Example:**
```python
GITHUB_REPO_OWNER = "qsb-it"
GITHUB_REPO_NAME = "tlrs-calculator"
```

### Step 4: Create GitHub Personal Access Token (Optional but Recommended)

For private repositories, you need an access token:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Settings:
   - **Note**: TLRS Calculator Updater
   - **Expiration**: No expiration (or 1 year)
   - **Scopes**: Check ✅ `repo` (Full control of private repositories)
4. Click "Generate token"
5. **COPY THE TOKEN** (you won't see it again!)

6. Edit `updater.py` line 20:
```python
GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Paste your token here
```

**Security Note:** The token will be embedded in the exe. For better security, consider:
- Using a read-only token
- Rotating tokens periodically
- Or skip token and require users to be logged into GitHub

---

## Creating a Release

### Step 1: Build the Executable

```cmd
pyinstaller tlrs.spec
```

The exe will be in `dist\QSB_TLRS_Calculator.exe`

### Step 2: Create Release on GitHub

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Fill in:
   - **Tag**: `v1.0.0` (must start with 'v')
   - **Release title**: `Version 1.0.0 - Initial Release`
   - **Description**: 
     ```
     ## What's New
     - Initial release
     - Grade-based reimbursement calculation
     - Holiday fetching from sabah.gov.my
     - Excel export with calendar view
     - Personal leave management
     
     ## Installation
     Download QSB_TLRS_Calculator.exe and run it.
     ```
4. **Attach files**: Drag and drop `QSB_TLRS_Calculator.exe`
5. Click "Publish release"

### Step 3: Test the Update

1. Change version in `settings.py`:
   ```python
   APP_VERSION = "0.9.0"  # Lower than release
   ```
2. Rebuild exe: `pyinstaller tlrs.spec`
3. Run the exe
4. Enable "Check for updates on startup" in Settings
5. Restart app - should show update dialog

---

## Releasing Updates

### When you have a new version:

1. **Update version** in `settings.py`:
   ```python
   APP_VERSION = "1.0.1"  # Increment version
   ```

2. **Rebuild executable**:
   ```cmd
   pyinstaller tlrs.spec
   ```

3. **Create new GitHub Release**:
   - Tag: `v1.0.1`
   - Title: `Version 1.0.1 - Bug Fixes`
   - Description: List changes
   - Attach: `QSB_TLRS_Calculator.exe`

4. **Users will be notified** on next app startup (if enabled in settings)

---

## Version Numbering

Use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR** (1.x.x): Breaking changes, major features
- **MINOR** (x.1.x): New features, backwards compatible
- **PATCH** (x.x.1): Bug fixes, small improvements

Examples:
- `1.0.0` - Initial release
- `1.0.1` - Bug fix
- `1.1.0` - New feature added
- `2.0.0` - Major redesign

---

## User Experience

### When update is available:

1. App starts normally
2. After 1 second, checks GitHub for updates (background)
3. If newer version found, shows dialog:
   - Current version
   - New version
   - Release notes
   - "Download & Install" button
4. User clicks "Download & Install":
   - Progress bar shows download
   - Automatically installs
   - App restarts with new version

### Settings Control

Users can enable/disable in Settings:
- ✅ Check for updates on startup

---

## Troubleshooting

### Update check fails
- Check internet connection
- Verify GitHub token is correct
- Ensure repository name matches in `updater.py`
- Check if user has access to private repo

### Download fails
- Check GitHub release has exe attached
- Verify exe filename ends with `.exe`
- Check file size isn't too large (GitHub limit: 2GB)

### Update doesn't apply
- Check Windows permissions
- Try running as administrator
- Antivirus might block the updater script

---

## Security Best Practices

1. **Code Signing**: Sign your exe to avoid Windows SmartScreen warnings
2. **Token Security**: Use read-only tokens, rotate periodically
3. **HTTPS Only**: GitHub uses HTTPS by default
4. **Access Control**: Only add trusted team members to repo
5. **Audit Releases**: Review who published each release

---

## Alternative: Without GitHub Token

If you don't want to embed a token:

1. Leave `GITHUB_TOKEN = ""` in `updater.py`
2. Users must be logged into GitHub in their browser
3. Or make repository public (not recommended for internal tools)

---

## Files Modified

- `updater.py` - New file, handles update checking and downloading
- `tlrs_gui_v2.py` - Added update check on startup
- `settings.py` - Already has "check_updates_on_start" setting

---

## Next Steps

1. ✅ Create private GitHub repository
2. ✅ Update `updater.py` with your repo name
3. ✅ Generate GitHub token (optional)
4. ✅ Create first release (v1.0.0)
5. ✅ Test update functionality
6. ✅ Distribute to QSB team

---

## Support

For issues or questions, contact QSB IT Team.
