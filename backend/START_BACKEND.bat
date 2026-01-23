@echo off
REM START BACKEND - Run this file to start the backend server
REM This sets up the environment correctly and starts the server

title Todo Backend Server
cd /d "%~dp0"

echo.
echo ========================================
echo TODO BACKEND - Starting Server
echo ========================================
echo.
echo Setting up Python environment...

REM Set PYTHONPATH to include src
set PYTHONPATH=%CD%\src;%PYTHONPATH%

echo PYTHONPATH: %PYTHONPATH%
echo.

REM Verify we're in the right directory
if not exist "src\core\config.py" (
    echo ERROR: src directory not found!
    echo Make sure you're running this from the backend folder
    pause
    exit /b 1
)

echo Checking Python packages...
python -m pip show openai >nul 2>&1
if errorlevel 1 (
    echo ERROR: openai package not installed
    echo Run: pip install openai langchain langchain-openai langchain-community
    pause
    exit /b 1
)

echo ✓ All checks passed
echo.
echo Starting server on http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
