@echo off
title IT Helpdesk Professional - GUI Launcher
echo.
echo ========================================
echo  IT Helpdesk Professional
echo  Enterprise Management Console
echo ========================================
echo.
echo Starting professional GUI launcher...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or later
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import tkinter, psutil, requests, PIL, flask, flask_sqlalchemy, flask_wtf" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install psutil requests Pillow flask flask-sqlalchemy flask-wtf flask-login email-validator openpyxl
)

REM Test the setup first
echo Testing server compatibility...
python test_server_windows.py
if errorlevel 1 (
    echo.
    echo Setup test failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Test passed! Launching IT Helpdesk Professional GUI...
python gui_launcher_professional.py

if errorlevel 1 (
    echo.
    echo Error occurred while running the GUI
    echo Falling back to standard GUI launcher...
    python gui_launcher.py
)

pause