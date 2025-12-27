"""
Setup script for creating standalone Email Generator Bot executable
Run this script to build a Windows executable (.exe) file
"""

import os
import sys
import subprocess

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Install PyInstaller using pip"""
    print("Installing PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")
        return True
    except Exception as e:
        print(f"✗ Error installing PyInstaller: {e}")
        return False

def build_executable():
    """Build the executable using PyInstaller"""
    print("\nBuilding Email Generator Bot executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",              # Create single executable file
        "--windowed",             # No console window
        "--name=EmailBot",  # Name of executable
        "--icon=NONE",            # No icon (can be added later)
        "--clean",                # Clean PyInstaller cache
        "email_generator_bot.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n✓ Build successful!")
        print(f"Executable location: {os.path.join(os.getcwd(), 'dist', 'EmailGeneratorBot.exe')}")
        return True
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        return False

def create_batch_file():
    """Create a batch file for easy launching"""
    batch_content = """@echo off
echo Starting Email Generator Bot...
python email_generator_bot.py
pause
"""
    
    try:
        with open("run_email_bot.bat", "w") as f:
            f.write(batch_content)
        print("✓ Batch file created: run_email_bot.bat")
        return True
    except Exception as e:
        print(f"✗ Error creating batch file: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("Email Generator Bot - Setup Script")
    print("=" * 60)
    print()
    
    # Check if source file exists
    if not os.path.exists("email_generator_bot.py"):
        print("✗ Error: email_generator_bot.py not found in current directory")
        return
    
    print("Choose setup option:")
    print("1. Build standalone executable (requires PyInstaller)")
    print("2. Create batch file for easy launching")
    print("3. Both")
    print("4. Exit")
    print()
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == "1":
        # Build executable
        if not check_pyinstaller():
            print("\nPyInstaller not found.")
            install = input("Install PyInstaller? (y/n): ").strip().lower()
            if install == 'y':
                if not install_pyinstaller():
                    return
            else:
                print("Cannot build executable without PyInstaller")
                return
        
        build_executable()
        
    elif choice == "2":
        # Create batch file
        create_batch_file()
        
    elif choice == "3":
        # Both
        if not check_pyinstaller():
            print("\nPyInstaller not found.")
            install = input("Install PyInstaller? (y/n): ").strip().lower()
            if install == 'y':
                if not install_pyinstaller():
                    print("Skipping executable build...")
                else:
                    build_executable()
            else:
                print("Skipping executable build...")
        else:
            build_executable()
        
        create_batch_file()
        
    elif choice == "4":
        print("Exiting setup...")
        return
    
    else:
        print("Invalid choice. Please run the script again.")
        return
    
    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nYou can now:")
    print("- Run: python email_generator_bot.py")
    if choice in ["1", "3"]:
        print("- Or use: dist/EmailGeneratorBot.exe")
    if choice in ["2", "3"]:
        print("- Or double-click: run_email_bot.bat")

if __name__ == "__main__":
    main()
