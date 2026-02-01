@echo off
REM MMU Auto-Login Bot - Background Runner
REM This script starts the auto-login bot in the background

echo Starting MMU Auto-Login Bot in background mode...
echo Logs will be saved to: mmu_login_bot.log
echo.
echo To stop the bot, close this window or press Ctrl+C
echo.

cd /d "%~dp0"
python auto_login_background.py

pause
