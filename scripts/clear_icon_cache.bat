@echo off
echo Clearing Windows Icon Cache...
taskkill /f /im explorer.exe
timeout /t 2 /nobreak >nul
cd /d %userprofile%\AppData\Local\Microsoft\Windows\Explorer
attrib -h IconCache.db
del IconCache.db
attrib -h iconcache_*.db
del iconcache_*.db
echo Icon cache cleared!
timeout /t 2 /nobreak >nul
start explorer.exe
echo Done! Please check your executable icon now.
pause
