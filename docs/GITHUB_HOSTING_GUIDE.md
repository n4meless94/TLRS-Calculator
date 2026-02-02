# 🚀 Hosting QSB TLRS Updates on GitHub Pages

This guide explains how to use a free GitHub repository to host your application updates.

## Phase 1: Create the Repository

1.  Log in to **GitHub.com**.
2.  Click **+** (top right) -> **New repository**.
3.  Name it: `qsb-tlrs-updates` (or similar).
4.  Select **Public** (required for free GitHub Pages, unless you have Pro).
    *   *Note: If you need it Private, you can still use the "Releases" feature, but this guide focuses on the simple "Pages/Raw" method.*
5.  Check **Initialize this repository with a README**.
6.  Click **Create repository**.

## Phase 2: Upload Files

You need to upload two files to the root of your repository:

### 1. `version.json`
Create a file named `version.json` on your computer or directly on GitHub with this content:
```json
{
    "version": "0.9.0",
    "download_url": "https://github.com/YOUR_USERNAME/qsb-tlrs-updates/releases/download/v0.9.0/QSB_TLRS_Calculator.exe",
    "release_notes": "Initial deployment on GitHub.",
    "published_at": "2026-02-03"
}
```
*(We will fix the `download_url` in Phase 3)*

### 2. The Application Executable
1.  Go to your repository page.
2.  Click **Add file** -> **Upload files**.
3.  Drag and drop your `dist/QSB_TLRS_Calculator.exe`.
4.  Commit changes.

## Phase 3: Get the URLs

### For `version.json` (The Checker)
1.  Click on `version.json` in the file list.
2.  Click the **Raw** button (top right of the file view).
3.  Copy the URL from your browser address bar.
    *   It should look like: `https://raw.githubusercontent.com/YourUser/qsb-tlrs-updates/main/version.json`
4.  **Paste this URL** into `updater.py` as the `VERSION_JSON_URL`.

### For the Executable (The Download)
**Option A: Direct File Hosting (Simplest)**
1.  Click on the `.exe` file in GitHub.
2.  Click the **Download** button (or "View Raw").
3.  Copy that URL.
    *   It typically redirects to a `raw.githubusercontent.com` link or a `objects.githubusercontent.com` link.
    *   *Better approach:* Use the "Releases" feature for the exe (see below), as raw links for binaries can sometimes be throttled.

**Option B: GitHub Releases (Recommended for Binaries)**
1.  On the repo main page, click **Releases** (on the right).
2.  "Create a new release".
3.  Tag version: `v0.9.0`.
4.  Title: `v0.9.0`.
5.  Upload `QSB_TLRS_Calculator.exe` to the "Attach binaries" section.
6.  Publish release.
7.  Right-click the asset link you just uploaded and "Copy link address".
    *   It looks like: `https://github.com/User/Repo/releases/download/v0.9.0/QSB_TLRS_Calculator.exe`
8.  **Paste this URL** into your `version.json` as the `download_url`.

## Phase 4: Finalize the App

1.  Update `updater.py` with the **Raw** URL for `version.json`.
2.  Rebuild your app:
    ```cmd
    py build_installer.py
    ```
3.  The new `installer_package` is now ready to distribute!
4.  When you want to push an update:
    *   Build new exe.
    *   Create new GitHub Release (v2.3.0) & upload exe.
    *   Edit `version.json` in the repo to point to v2.3.0.
    *   Users' apps will see the change in `version.json` and auto-update!
