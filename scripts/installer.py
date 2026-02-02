#!/usr/bin/env python3
"""
QSB TLRS Calculator Installer
Installs the application to %LOCALAPPDATA% with Start Menu shortcuts
"""

import os
import sys
import shutil
import winshell
from pathlib import Path
import subprocess

# Installation constants
APP_NAME = "QSB TLRS Calculator"
APP_FOLDER = "QSB_TLRS"
EXECUTABLE_NAME = "QSB_TLRS_Calculator.exe"

def get_install_dir():
    """Get the installation directory in %LOCALAPPDATA%"""
    return Path(os.getenv('LOCALAPPDATA')) / APP_FOLDER

def get_start_menu_dir():
    """Get Start Menu programs directory"""
    return Path(winshell.programs()) / APP_NAME

def create_directories():
    """Create necessary directories"""
    install_dir = get_install_dir()
    install_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created installation directory: {install_dir}")
    return install_dir

def copy_files(install_dir):
    """Copy application files to installation directory"""
    # Get the directory where the installer script is located
    script_dir = Path(__file__).parent
    
    # Files to copy
    files_to_copy = [
        "QSB_TLRS_Calculator.exe",
        "qsb_tlrs.ico",
        # Add any other required files
    ]
    
    for file_name in files_to_copy:
        source = script_dir / file_name
        if source.exists():
            destination = install_dir / file_name
            shutil.copy2(source, destination)
            print(f"✓ Copied {file_name}")
        else:
            print(f"⚠ Warning: {file_name} not found in {script_dir}")

def create_start_menu_shortcut(install_dir):
    """Create Start Menu shortcut"""
    try:
        start_menu_dir = get_start_menu_dir()
        start_menu_dir.mkdir(parents=True, exist_ok=True)
        
        shortcut_path = start_menu_dir / f"{APP_NAME}.lnk"
        executable_path = install_dir / EXECUTABLE_NAME
        icon_path = install_dir / "qsb_tlrs.ico"
        
        # Create shortcut using winshell
        winshell.CreateShortcut(
            Path=str(shortcut_path),
            Target=str(executable_path),
            Icon=(str(icon_path), 0),
            Description="Transport Lease Reimbursement Scheme Calculator"
        )
        
        print(f"✓ Created Start Menu shortcut: {shortcut_path}")
        return True
        
    except Exception as e:
        print(f"⚠ Could not create Start Menu shortcut: {e}")
        return False

def create_desktop_shortcut(install_dir):
    """Create Desktop shortcut (optional)"""
    try:
        desktop = Path(winshell.desktop())
        shortcut_path = desktop / f"{APP_NAME}.lnk"
        executable_path = install_dir / EXECUTABLE_NAME
        icon_path = install_dir / "qsb_tlrs.ico"
        
        winshell.CreateShortcut(
            Path=str(shortcut_path),
            Target=str(executable_path),
            Icon=(str(icon_path), 0),
            Description="Transport Lease Reimbursement Scheme Calculator"
        )
        
        print(f"✓ Created Desktop shortcut: {shortcut_path}")
        return True
        
    except Exception as e:
        print(f"⚠ Could not create Desktop shortcut: {e}")
        return False

def register_uninstaller(install_dir):
    """Create uninstaller script"""
    uninstaller_content = f'''#!/usr/bin/env python3
"""
QSB TLRS Calculator Uninstaller
"""

import os
import shutil
from pathlib import Path
import winshell

APP_NAME = "{APP_NAME}"
INSTALL_DIR = Path(r"{install_dir}")

def remove_shortcuts():
    """Remove Start Menu and Desktop shortcuts"""
    try:
        # Remove Start Menu folder
        start_menu_dir = Path(winshell.programs()) / APP_NAME
        if start_menu_dir.exists():
            shutil.rmtree(start_menu_dir)
            print("✓ Removed Start Menu shortcuts")
        
        # Remove Desktop shortcut
        desktop_shortcut = Path(winshell.desktop()) / f"{APP_NAME}.lnk"
        if desktop_shortcut.exists():
            desktop_shortcut.unlink()
            print("✓ Removed Desktop shortcut")
            
    except Exception as e:
        print(f"⚠ Error removing shortcuts: {{e}}")

def main():
    print(f"Uninstalling {{APP_NAME}}...")
    
    # Remove shortcuts
    remove_shortcuts()
    
    # Remove installation directory
    if INSTALL_DIR.exists():
        shutil.rmtree(INSTALL_DIR)
        print(f"✓ Removed installation directory: {{INSTALL_DIR}}")
    
    print("\\nUninstallation complete!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
'''
    
    uninstaller_path = install_dir / "uninstall.py"
    with open(uninstaller_path, 'w', encoding='utf-8') as f:
        f.write(uninstaller_content)
    
    print(f"✓ Created uninstaller: {uninstaller_path}")

def main():
    """Main installation process"""
    print(f"Installing {APP_NAME}...")
    print("=" * 50)
    
    # Check if winshell is available
    try:
        import winshell
    except ImportError:
        print("Error: winshell module is required for creating shortcuts")
        print("Install it with: pip install winshell")
        sys.exit(1)
    
    # Create installation directory
    install_dir = create_directories()
    
    # Copy application files
    copy_files(install_dir)
    
    # Create shortcuts
    start_menu_created = create_start_menu_shortcut(install_dir)
    
    # Ask about desktop shortcut
    create_desktop = input("\\nCreate Desktop shortcut? (y/N): ").lower().startswith('y')
    if create_desktop:
        create_desktop_shortcut(install_dir)
    
    # Create uninstaller
    register_uninstaller(install_dir)
    
    print("\\n" + "=" * 50)
    print(f"✓ Installation complete!")
    print(f"✓ Installed to: {install_dir}")
    
    if start_menu_created:
        print(f"✓ You can now find '{APP_NAME}' in your Start Menu")
    
    print(f"\\nTo uninstall, run: python \"{install_dir / 'uninstall.py'}\"")
    
    # Ask to launch the application
    launch = input("\\nLaunch the application now? (Y/n): ").lower()
    if not launch.startswith('n'):
        executable_path = install_dir / EXECUTABLE_NAME
        if executable_path.exists():
            subprocess.Popen([str(executable_path)])
            print("✓ Application launched!")

if __name__ == "__main__":
    main()