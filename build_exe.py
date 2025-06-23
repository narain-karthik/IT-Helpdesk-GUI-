#!/usr/bin/env python3
"""
Build script for creating executable package of GTN Engineering IT Helpdesk
Creates a complete standalone application with all dependencies
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_spec_file():
    """Create PyInstaller spec file for the application"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Add all Python files and dependencies
a = Analysis(
    ['gui_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
        ('*.py', '.'),
        ('*.md', '.'),
        ('*.txt', '.'),
        ('*.toml', '.'),
        ('*.lock', '.'),
    ],
    hiddenimports=[
        'flask',
        'flask_sqlalchemy',
        'flask_wtf',
        'flask_login',
        'werkzeug',
        'email_validator',
        'openpyxl',
        'psycopg2',
        'gunicorn',
        'requests',
        'psutil',
        'pillow',
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'threading',
        'subprocess',
        'json',
        'webbrowser',
        'datetime',
        'time',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GTN_Helpdesk_Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='static/favicon.ico' if os.path.exists('static/favicon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GTN_Helpdesk_System',
)
'''
    
    with open('helpdesk.spec', 'w') as f:
        f.write(spec_content)
    
    print("✓ Created PyInstaller spec file")

def create_icon():
    """Create application icon from logo"""
    try:
        from PIL import Image
        
        if os.path.exists('static/gtn_logo.jpg'):
            # Convert logo to icon
            img = Image.open('static/gtn_logo.jpg')
            img = img.resize((256, 256), Image.Resampling.LANCZOS)
            
            # Ensure static directory exists
            os.makedirs('static', exist_ok=True)
            
            # Save as ICO file for Windows
            img.save('static/favicon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
            print("✓ Created application icon")
        else:
            print("! Logo file not found, skipping icon creation")
            
    except ImportError:
        print("! Pillow not available, skipping icon creation")
    except Exception as e:
        print(f"! Error creating icon: {e}")

def create_installer_script():
    """Create installation script"""
    installer_content = '''@echo off
echo ===============================================
echo GTN Engineering IT Helpdesk System Installer
echo ===============================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges...
) else (
    echo WARNING: Not running as administrator
    echo Some features may not work properly
    echo.
)

echo Installing GTN Engineering IT Helpdesk System...
echo.

REM Create installation directory
set INSTALL_DIR=%ProgramFiles%\\GTN Engineering\\IT Helpdesk
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files
echo Copying application files...
xcopy /E /I /Y "GTN_Helpdesk_System" "%INSTALL_DIR%"

REM Create desktop shortcut
echo Creating desktop shortcut...
set SHORTCUT_PATH=%USERPROFILE%\\Desktop\\GTN IT Helpdesk.lnk
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%INSTALL_DIR%\\GTN_Helpdesk_Launcher.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%INSTALL_DIR%\\GTN_Helpdesk_Launcher.exe'; $Shortcut.Description = 'GTN Engineering IT Helpdesk System'; $Shortcut.Save()"

REM Create start menu entry
echo Creating start menu entry...
set STARTMENU_DIR=%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs\\GTN Engineering
if not exist "%STARTMENU_DIR%" mkdir "%STARTMENU_DIR%"
set STARTMENU_SHORTCUT=%STARTMENU_DIR%\\GTN IT Helpdesk.lnk
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTMENU_SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\\GTN_Helpdesk_Launcher.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%INSTALL_DIR%\\GTN_Helpdesk_Launcher.exe'; $Shortcut.Description = 'GTN Engineering IT Helpdesk System'; $Shortcut.Save()"

echo.
echo ===============================================
echo Installation completed successfully!
echo ===============================================
echo.
echo You can now run the application from:
echo - Desktop shortcut: GTN IT Helpdesk
echo - Start Menu: GTN Engineering ^> GTN IT Helpdesk
echo - Direct path: %INSTALL_DIR%\\GTN_Helpdesk_Launcher.exe
echo.
echo Press any key to exit...
pause >nul
'''
    
    with open('install.bat', 'w') as f:
        f.write(installer_content)
    
    print("✓ Created installation script")

def create_uninstaller():
    """Create uninstallation script"""
    uninstaller_content = '''@echo off
echo ===============================================
echo GTN Engineering IT Helpdesk System Uninstaller
echo ===============================================
echo.

set INSTALL_DIR=%ProgramFiles%\\GTN Engineering\\IT Helpdesk

echo Removing GTN Engineering IT Helpdesk System...
echo.

REM Remove desktop shortcut
if exist "%USERPROFILE%\\Desktop\\GTN IT Helpdesk.lnk" (
    echo Removing desktop shortcut...
    del "%USERPROFILE%\\Desktop\\GTN IT Helpdesk.lnk"
)

REM Remove start menu entry
if exist "%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs\\GTN Engineering\\GTN IT Helpdesk.lnk" (
    echo Removing start menu entry...
    del "%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs\\GTN Engineering\\GTN IT Helpdesk.lnk"
    rmdir "%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs\\GTN Engineering" 2>nul
)

REM Remove application files
if exist "%INSTALL_DIR%" (
    echo Removing application files...
    rmdir /S /Q "%INSTALL_DIR%"
    rmdir "%ProgramFiles%\\GTN Engineering" 2>nul
)

echo.
echo ===============================================
echo Uninstallation completed successfully!
echo ===============================================
echo.
echo Press any key to exit...
pause >nul
'''
    
    with open('GTN_Helpdesk_System/uninstall.bat', 'w') as f:
        f.write(uninstaller_content)
    
    print("✓ Created uninstallation script")

def create_readme():
    """Create README for the executable package"""
    readme_content = '''# GTN Engineering IT Helpdesk System - Executable Package

## What's Included

This package contains a complete, standalone installation of the GTN Engineering IT Helpdesk System.

### Package Contents:
- GTN_Helpdesk_Launcher.exe - Main application launcher
- All required Python libraries and dependencies
- Web application files (templates, static files)
- Configuration management
- Database connectivity tools
- Installation and uninstallation scripts

## Installation

### Automatic Installation (Recommended)
1. Run `install.bat` as Administrator
2. Follow the installation prompts
3. The application will be installed to Program Files
4. Desktop and Start Menu shortcuts will be created

### Manual Installation
1. Extract the entire `GTN_Helpdesk_System` folder to your desired location
2. Run `GTN_Helpdesk_Launcher.exe` from the extracted folder

## First Time Setup

1. Launch the application using the desktop shortcut or Start Menu
2. Go to the "Database Config" tab
3. Enter your PostgreSQL database connection details:
   - Host: Your PostgreSQL server address
   - Port: Usually 5432
   - Database Name: Your database name
   - Username: Database username
   - Password: Database password
4. Click "Test Connection" to verify settings
5. Click "Save Configuration"
6. Go to the "Server Management" tab
7. Click "Start Server" to launch the web application
8. Click "Open in Browser" to access the helpdesk system

## System Requirements

### Minimum Requirements:
- Windows 10 or later (64-bit)
- 2 GB RAM
- 500 MB free disk space
- PostgreSQL database server (local or remote)

### Recommended:
- Windows 11 (64-bit)
- 4 GB RAM
- 1 GB free disk space
- Dedicated PostgreSQL server

## Database Setup

### Option 1: Use Existing PostgreSQL Server
- Connect to your existing PostgreSQL installation
- Create a new database for the helpdesk system
- Use those credentials in the application

### Option 2: Install PostgreSQL Locally
1. Download PostgreSQL from https://www.postgresql.org/download/
2. Install with default settings
3. Remember the password you set for the 'postgres' user
4. Create a new database called 'gtn_helpdesk'
5. Use these credentials in the application

## Using the Application

### For Administrators:
1. Start the GTN Helpdesk Launcher
2. Configure database connection
3. Start the server
4. Access the web interface through your browser
5. Log in with Super Admin credentials (change default password immediately)
6. Create user accounts for your team

### For End Users:
- Access the helpdesk system through a web browser
- URL will be displayed in the launcher (typically http://localhost:5000)
- Create tickets, track progress, communicate with IT team

## Features

- Complete ticket management system
- Role-based access control (Users, Admins, Super Admins)
- Image upload support for tickets
- Real-time status tracking
- Reporting and analytics
- Excel export functionality
- System information capture
- Comment system for collaboration

## Troubleshooting

### Application Won't Start
- Ensure you have administrator privileges
- Check if antivirus software is blocking the application
- Verify all files were extracted properly

### Database Connection Issues
- Verify PostgreSQL is running
- Check firewall settings
- Confirm database credentials
- Test connection using the built-in test feature

### Server Won't Start
- Check if port 5000 is available
- Try changing the server port in settings
- Ensure no other web servers are running
- Check Windows Firewall settings

### Browser Issues
- Try a different web browser
- Clear browser cache and cookies
- Disable browser extensions temporarily
- Check if popup blockers are interfering

## Support

For technical support:
- Use the built-in helpdesk system once operational
- Contact your IT administrator
- Check the application logs in the "Logs" tab

## Security Notes

- Change all default passwords immediately after installation
- Use strong passwords for database connections
- Regularly backup your database
- Keep the application updated
- Monitor user access and permissions

## Uninstallation

To remove the application:
1. Close the GTN Helpdesk Launcher if running
2. Run the uninstall.bat script as Administrator
3. Or manually delete the installation folder and shortcuts

## Version Information

Version: 2.1.0
Build Date: June 23, 2025
Python Version: 3.11+
Framework: Flask with Gunicorn

---

GTN Engineering IT Helpdesk System
Professional IT Support Management Solution
'''
    
    with open('GTN_Helpdesk_System/README.txt', 'w') as f:
        f.write(readme_content)
    
    print("✓ Created package README")

def build_executable():
    """Build the executable using PyInstaller"""
    try:
        print("Building executable package...")
        print("This may take several minutes...")
        
        # Run PyInstaller
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--noconfirm',
            'helpdesk.spec'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Executable built successfully")
            return True
        else:
            print(f"✗ Build failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Build error: {e}")
        return False

def create_distribution_package():
    """Create final distribution package"""
    try:
        dist_dir = "GTN_Helpdesk_Distribution"
        
        # Remove existing distribution
        if os.path.exists(dist_dir):
            shutil.rmtree(dist_dir)
        
        # Create distribution directory
        os.makedirs(dist_dir)
        
        # Copy built application
        if os.path.exists("dist/GTN_Helpdesk_System"):
            shutil.copytree("dist/GTN_Helpdesk_System", f"{dist_dir}/GTN_Helpdesk_System")
        else:
            print("✗ Built application not found")
            return False
        
        # Copy installation scripts
        shutil.copy("install.bat", dist_dir)
        
        # Create uninstaller in the app directory
        create_uninstaller()
        
        # Create package README
        create_readme()
        
        # Create distribution README
        dist_readme = '''# GTN Engineering IT Helpdesk System - Distribution Package

## Quick Start

1. Run `install.bat` as Administrator for automatic installation
2. Or extract `GTN_Helpdesk_System` folder and run manually
3. See `GTN_Helpdesk_System/README.txt` for detailed instructions

## Package Contents

- `GTN_Helpdesk_System/` - Complete application with all dependencies
- `install.bat` - Automatic installer for Windows
- `README.txt` - This file

## Installation Options

### Option 1: Automatic Installation (Recommended)
- Right-click `install.bat` and select "Run as Administrator"
- Follow the prompts
- Application will be installed to Program Files with shortcuts

### Option 2: Portable Installation
- Extract `GTN_Helpdesk_System` folder to desired location
- Run `GTN_Helpdesk_Launcher.exe` directly
- No installation required, fully portable

## System Requirements

- Windows 10/11 (64-bit)
- 2+ GB RAM
- PostgreSQL database (local or remote)

For detailed setup instructions, see `GTN_Helpdesk_System/README.txt`

---
GTN Engineering IT Helpdesk System v2.1.0
'''
        
        with open(f"{dist_dir}/README.txt", 'w') as f:
            f.write(dist_readme)
        
        print(f"✓ Distribution package created: {dist_dir}")
        
        # Create ZIP archive
        print("Creating ZIP archive...")
        shutil.make_archive("GTN_Helpdesk_Complete_Package", 'zip', dist_dir)
        print("✓ ZIP archive created: GTN_Helpdesk_Complete_Package.zip")
        
        return True
        
    except Exception as e:
        print(f"✗ Distribution package creation failed: {e}")
        return False

def main():
    """Main build process"""
    print("===============================================")
    print("GTN Engineering IT Helpdesk - Executable Builder")
    print("===============================================")
    print()
    
    # Check if PyInstaller is available
    try:
        import PyInstaller
        print("✓ PyInstaller is available")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    # Create necessary files
    create_icon()
    create_spec_file()
    create_installer_script()
    
    # Build executable
    if build_executable():
        # Create distribution package
        if create_distribution_package():
            print()
            print("===============================================")
            print("BUILD COMPLETED SUCCESSFULLY!")
            print("===============================================")
            print()
            print("Distribution package: GTN_Helpdesk_Distribution/")
            print("ZIP archive: GTN_Helpdesk_Complete_Package.zip")
            print()
            print("To distribute:")
            print("1. Share the ZIP file with end users")
            print("2. Users run install.bat as Administrator")
            print("3. Application installs with shortcuts")
            print()
            print("The package includes:")
            print("- Complete standalone application")
            print("- All Python dependencies")
            print("- Installation/uninstallation scripts")
            print("- User documentation")
            print("- GUI launcher with database configuration")
        else:
            print("✗ Distribution package creation failed")
    else:
        print("✗ Executable build failed")
    
    print()
    print("Press Enter to exit...")
    input()

if __name__ == "__main__":
    main()