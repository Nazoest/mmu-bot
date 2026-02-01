@echo off
REM Helper script to set environment variables for MMU Student Portal bots
REM Run this before running any of the bot scripts

echo ====================================
echo MMU Student Portal - Environment Setup
echo ====================================
echo.
echo This script will help you set your credentials as environment variables.
echo Your credentials will only be set for this terminal session.
echo.
echo NOTE: For permanent setup, create a .env file instead (see .env.example)
echo.

set /p REG_NUM="Enter your registration number (e.g., cit-223-101/2023): "
set MMU_REG_NUMBER=%REG_NUM%

set /p PWD="Enter your password: "
set MMU_PASSWORD=%PWD%

echo.
echo ====================================
echo Environment variables set!
echo ====================================
echo.
echo You can now run any of the bot scripts:
echo   - python student_portal_login.py
echo   - python auto_login_background.py
echo   - python unit_registration.py
echo   - python course_registration_bot.py
echo.
echo NOTE: These credentials are only valid for this terminal session.
echo To set them permanently, create a .env file (copy from .env.example)
echo.
pause
