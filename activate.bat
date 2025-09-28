@echo off
REM Activation script for Picky Meal Planner (Windows Command Prompt/PowerShell)

echo 🍽️  Activating Picky Meal Planner environment...
call venv\Scripts\activate
echo ✅ Virtual environment activated!
echo 📦 Installed packages:
pip list | findstr /R "flask cors python-dotenv"
echo.
echo 🚀 To start the app, run: python run.py
echo 🛑 To deactivate, run: deactivate