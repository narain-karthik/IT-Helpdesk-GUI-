@echo off
title IT Helpdesk System
cd /d "%~dp0"

REM Hide console window and start GUI
if "%1"=="hidden" goto :start_hidden

start "" "%~f0" hidden
exit /b

:start_hidden
python gui_launcher.py
exit /b