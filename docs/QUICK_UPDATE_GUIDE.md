# Quick Update Release Guide

## Before First Use

1. Edit `updater.py`:
   ```python
   GITHUB_REPO_OWNER = "your-username"  # Line 18
   GITHUB_REPO_NAME = "tlrs-calculator"  # Line 19
   GITHUB_TOKEN = "ghp_your_token_here"  # Line 20 (optional)
   ```

2. Create private GitHub repo: `your-username/tlrs-calculator`

3. Add team members as collaborators

## Releasing New Version

### 1. Update Version
Edit `settings.py`:
```python
APP_VERSION = "1.0.1"  # Increment this
```

### 2. Build
```cmd
pyinstaller tlrs.spec
```

### 3. Create GitHub Release
- Go to: `https://github.com/your-username/tlrs-calculator/releases/new`
- Tag: `v1.0.1` (must match version with 'v' prefix)
- Title: `Version 1.0.1 - Description`
- Upload: `dist\QSB_TLRS_Calculator.exe`
- Click "Publish release"

### 4. Done!
Users will see update notification on next app start (if enabled in Settings).

---

## Version Format
- `1.0.0` → `1.0.1` (bug fix)
- `1.0.0` → `1.1.0` (new feature)
- `1.0.0` → `2.0.0` (major change)

---

## Testing Updates
1. Set lower version in `settings.py`: `APP_VERSION = "0.9.0"`
2. Rebuild: `pyinstaller tlrs.spec`
3. Run exe - should show update dialog
4. Click "Download & Install" - should update automatically
