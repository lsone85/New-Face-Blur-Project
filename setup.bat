@echo off
REM Setup script for Face Blur Project on Windows
REM Compatible with Python 3.9+ and PyCharm 2024.2.6

echo === Face Blur Project Setup Script ===
echo Setting up for Python 3.9+ and PyCharm compatibility

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found. Please install Python 3.9 or higher from python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Display Python version
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ✓ Setup completed successfully!
    echo.
    echo To run the application:
    echo   1. Activate the virtual environment: venv\Scripts\activate.bat
    echo   2. Run the application: python main.py
    echo.
    echo To run in PyCharm:
    echo   1. Open the project folder in PyCharm 2024.2.6
    echo   2. Configure Python interpreter to use: .\venv\Scripts\python.exe
    echo   3. Run main.py
    echo.
    echo Test compatibility: python test_compatibility.py
    echo.
) else (
    echo Error: Failed to install dependencies
    echo Check the error messages above and resolve any issues
)

pause