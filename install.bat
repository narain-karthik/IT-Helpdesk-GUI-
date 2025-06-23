@echo off
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
set INSTALL_DIR=%ProgramFiles%\GTN Engineering\IT Helpdesk
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files
echo Copying application files...
xcopy /E /I /Y "GTN_Helpdesk_System" "%INSTALL_DIR%"

REM Create desktop shortcut
echo Creating desktop shortcut...
set SHORTCUT_PATH=%USERPROFILE%\Desktop\GTN IT Helpdesk.lnk
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%INSTALL_DIR%\GTN_Helpdesk_Launcher.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%INSTALL_DIR%\GTN_Helpdesk_Launcher.exe'; $Shortcut.Description = 'GTN Engineering IT Helpdesk System'; $Shortcut.Save()"

REM Create start menu entry
echo Creating start menu entry...
set STARTMENU_DIR=%ProgramData%\Microsoft\Windows\Start Menu\Programs\GTN Engineering
if not exist "%STARTMENU_DIR%" mkdir "%STARTMENU_DIR%"
set STARTMENU_SHORTCUT=%STARTMENU_DIR%\GTN IT Helpdesk.lnk
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTMENU_SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\GTN_Helpdesk_Launcher.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%INSTALL_DIR%\GTN_Helpdesk_Launcher.exe'; $Shortcut.Description = 'GTN Engineering IT Helpdesk System'; $Shortcut.Save()"

echo.
echo ===============================================
echo Installation completed successfully!
echo ===============================================
echo.
echo You can now run the application from:
echo - Desktop shortcut: GTN IT Helpdesk
echo - Start Menu: GTN Engineering ^> GTN IT Helpdesk
echo - Direct path: %INSTALL_DIR%\GTN_Helpdesk_Launcher.exe
echo.
echo Press any key to exit...
pause >nul
