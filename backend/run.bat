@echo off
REM Windows Batch Script to Run Backend

cd "\\wsl.localhost\Ubuntu-24.04\home\yusraa\Phase-3\Phase-3\backend"

REM Set PYTHONPATH to include src directory  
set PYTHONPATH=%CD%\src;%PYTHONPATH%

echo.
echo ================================
echo Starting Backend Server
echo ================================
echo PYTHONPATH: %PYTHONPATH%
echo.

REM Run uvicorn with PYTHONPATH set
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
