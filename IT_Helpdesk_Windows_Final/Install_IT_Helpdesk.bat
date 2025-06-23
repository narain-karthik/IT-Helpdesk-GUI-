@echo off
title IT Helpdesk Installer

echo ============================
echo IT Helpdesk System Installer
echo ============================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.11+ from python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Installing IT Helpdesk System...
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create Program Files directory
set "INSTALL_DIR=%ProgramFiles%\IT Helpdesk"
net session >nul 2>&1
if %errorlevel% neq 0 (
    set "INSTALL_DIR=%LOCALAPPDATA%\IT Helpdesk"
    echo Installing to user directory: %INSTALL_DIR%
) else (
    echo Installing to: %INSTALL_DIR%
)

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files
echo Copying application files...
xcopy /E /I /Y /Q * "%INSTALL_DIR%\"

REM Create desktop shortcut
echo Creating desktop shortcut...
set "SHORTCUT=%USERPROFILE%\Desktop\IT Helpdesk.lnk"
powershell -command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%SHORTCUT%'); $SC.TargetPath = '%INSTALL_DIR%\IT_Helpdesk.bat'; $SC.WorkingDirectory = '%INSTALL_DIR%'; $SC.Description = 'IT Helpdesk System'; $SC.Save()"

REM Create Start Menu entry
set "STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
if not exist "%STARTMENU%" set "STARTMENU=%ProgramData%\Microsoft\Windows\Start Menu\Programs"
set "STARTMENU_SHORTCUT=%STARTMENU%\IT Helpdesk.lnk"
powershell -command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%STARTMENU_SHORTCUT%'); $SC.TargetPath = '%INSTALL_DIR%\IT_Helpdesk.bat'; $SC.WorkingDirectory = '%INSTALL_DIR%'; $SC.Description = 'IT Helpdesk System'; $SC.Save()"

echo.
echo ============================
echo Installation Complete!
echo ============================
echo.
echo IT Helpdesk has been installed successfully!
echo.
echo You can now start the application:
echo - Desktop shortcut: IT Helpdesk
echo - Start Menu: IT Helpdesk
echo.
echo Next steps:
echo 1. Click the desktop shortcut to launch IT Helpdesk
echo 2. Configure your PostgreSQL database connection
echo 3. Start the server and access via web browser
echo.
pause