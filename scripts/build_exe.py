import os
import shutil
import subprocess
import sys

def main():
    print(">>> Starting Build Process...")
    
    # Configuration
    APP_NAME = "QSB Working Day Calendar"
    MAIN_SCRIPT = "main.py"
    ICON_PATH = "" # Add icon if available, else standard
    
    # Cleanup
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            print(f">>> Cleaning {folder}...")
            shutil.rmtree(folder)
    
    if os.path.exists(f"{APP_NAME}.spec"):
        os.remove(f"{APP_NAME}.spec")

    # PyInstaller Command
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--clean",
        "--windowed",      # No console window
        "--onefile",       # Single EXE
        "--name", APP_NAME,
        "--hidden-import", "babel.numbers", # Often missed
        "--collect-all", "reportlab",       # Ensure reportlab resources are there
        MAIN_SCRIPT
    ]
    
    print(f">>> Running: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("\n>>> Build Successful!")
        print(f">>> Executable is located in: {os.path.abspath('dist')}")
        
        # Open dist folder
        os.startfile("dist")
        
    except subprocess.CalledProcessError as e:
        print(f"\n>>> Build Failed with error code {e.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
