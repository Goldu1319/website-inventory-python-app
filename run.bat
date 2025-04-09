@echo off
echo Starting Inventory Management System...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.x
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking required packages...
pip install -r requirements.txt

REM Start the Flask application
echo.
echo Starting the application...
echo.
python app.py

pause 