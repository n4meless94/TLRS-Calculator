#!/usr/bin/env python3
"""
Build script for QSB TLRS Calculator
Creates both the executable and installer
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    print(f"Running: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error: {description} failed")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return False
    
    print(f"✅ {description} completed successfully")
    return True

def check_dependencies():
    """Check if required tools are installed"""
    print("Checking dependencies...")
    
    # Check PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False
    
    # Check openpyxl
    try:
        import openpyxl
        print("✅ openpyxl found")
    except ImportError:
        print("❌ openpyxl not found. Install with: pip install openpyxl")
        return False
    
    # Check winshell (for installer)
    try:
        import winshell
        print("✅ winshell found")
    except ImportError:
        print("❌ winshell not found. Install with: pip install winshell")
        return False
    
    return True

def build_executable():
    """Build the main executable using PyInstaller"""
    if not Path("tlrs.spec").exists():
        print("❌ tlrs.spec not found")
        return False
    
    return run_command(
        ["py", "-m", "PyInstaller", "tlrs.spec"],
        "Building executable"
    )

def create_installer_package():
    """Create installer package with all necessary files"""
    print("\nCreating installer package...")
    
    # Create installer directory
    installer_dir = Path("installer_package")
    if installer_dir.exists():
        try:
            shutil.rmtree(installer_dir)
        except PermissionError:
            print("⚠ Cannot remove existing installer_package (files may be in use)")
            print("  Trying to clean and reuse...")
            # Try to remove files individually
            for item in installer_dir.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                except:
                    pass
    
    installer_dir.mkdir(exist_ok=True)
    
    # Copy executable
    exe_source = Path("dist/QSB_TLRS_Calculator.exe")
    if not exe_source.exists():
        print("❌ QSB_TLRS_Calculator.exe not found in dist/")
        return False
    
    shutil.copy2(exe_source, installer_dir / "QSB_TLRS_Calculator.exe")
    print("✅ Copied QSB_TLRS_Calculator.exe")
    
    # Copy icon
    icon_source = Path("assets/qsb_tlrs.ico")
    if icon_source.exists():
        shutil.copy2(icon_source, installer_dir / "qsb_tlrs.ico")
        print("✅ Copied icon")
    
    # Copy installer script
    shutil.copy2("scripts/installer.py", installer_dir / "installer.py")
    print("✅ Copied installer.py")
    
    # Create README for installer
    readme_content = """# QSB TLRS Calculator Installer

## Installation Instructions:

1. Make sure Python is installed on your system
2. Install required dependency: pip install winshell
3. Run: python installer.py

The installer will:
- Install the application to %LOCALAPPDATA%\\QSB_TLRS\\
- Create Start Menu shortcuts
- Optionally create Desktop shortcut
- Set up auto-updater (no admin rights needed)

## For IT Departments:

You can distribute this installer_package folder to users.
The application installs to user space, so no admin rights are required.

## Auto-Updates:

Once installed, the application can auto-update from SharePoint/OneDrive
without requiring admin privileges.
"""
    
    with open(installer_dir / "README.txt", 'w') as f:
        f.write(readme_content)
    print("✅ Created README.txt")
    
    print(f"✅ Installer package created in: {installer_dir}")
    return True

def create_portable_version():
    """Create portable version (current behavior)"""
    print("\nCreating portable version...")
    
    portable_dir = Path("portable_version")
    if portable_dir.exists():
        try:
            shutil.rmtree(portable_dir)
        except PermissionError:
            print("⚠ Cannot remove existing portable_version (files may be in use)")
            print("  Trying to clean and reuse...")
            for item in portable_dir.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                except:
                    pass
    
    portable_dir.mkdir(exist_ok=True)
    
    # Copy executable
    exe_source = Path("dist/QSB_TLRS_Calculator.exe")
    shutil.copy2(exe_source, portable_dir / "QSB_TLRS_Calculator.exe")
    
    # Copy icon
    icon_source = Path("assets/qsb_tlrs.ico")
    if icon_source.exists():
        shutil.copy2(icon_source, portable_dir / "qsb_tlrs.ico")
    
    # Create portable README
    portable_readme = """# QSB TLRS Calculator (Portable)

This is the portable version. Simply run QSB_TLRS_Calculator.exe to start the application.

No installation required - you can run it from any folder.
Settings will be saved in the same directory as the executable.
"""
    
    with open(portable_dir / "README.txt", 'w') as f:
        f.write(portable_readme)
    
    print(f"✅ Portable version created in: {portable_dir}")
    return True

def main():
    """Main build process"""
    print("QSB TLRS Calculator Build Script")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Build executable
    if not build_executable():
        sys.exit(1)
    
    # Create installer package
    if not create_installer_package():
        sys.exit(1)
    
    # Create portable version
    if not create_portable_version():
        sys.exit(1)
    
    print("\n" + "=" * 40)
    print("✅ Build completed successfully!")
    print("\nOutput:")
    print("  📁 installer_package/ - For installation with shortcuts")
    print("  📁 portable_version/ - For portable use")
    print("  📁 dist/ - Raw PyInstaller output")
    
    print("\nDistribution options:")
    print("  • Share installer_package/ for users who want proper installation")
    print("  • Share portable_version/ for users who prefer portable apps")
    print("  • Both versions support auto-updates!")

if __name__ == "__main__":
    main()