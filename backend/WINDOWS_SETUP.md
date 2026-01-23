# Backend Running Guide for Windows

## Problem
You're running Windows with Python, accessing files via WSL path (\\wsl.localhost\...). The backend fails to start with:
```
No module named 'openai'
```

## Why
When you run `python -m uvicorn main:app`, Python doesn't know about the `src` directory where the backend code lives. All imports fail with "No module named..." errors.

## Solution

### Option 1: Set PYTHONPATH in PowerShell (RECOMMENDED)
```powershell
cd "\\wsl.localhost\Ubuntu-24.04\home\yusraa\Phase-3\Phase-3\backend"
$env:PYTHONPATH = "${PWD}\src;$env:PYTHONPATH"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Use the Batch File
```cmd
cd "\\wsl.localhost\Ubuntu-24.04\home\yusraa\Phase-3\Phase-3\backend"
run.bat
```

### Option 3: Run Python Script
```powershell
cd "\\wsl.localhost\Ubuntu-24.04\home\yusraa\Phase-3\Phase-3\backend"
python run_backend.py
```

### Option 4: Manual Command in CMD
```cmd
cd "\\wsl.localhost\Ubuntu-24.04\home\yusraa\Phase-3\Phase-3\backend"
set PYTHONPATH=%CD%\src;%PYTHONPATH%
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Testing It Works

Once the backend is running, in another terminal:
```powershell
curl http://localhost:8000/health
```

Should return:
```json
{"status":"healthy","app":"Todo Backend API","version":"3.0.0","debug":true}
```

## Required Dependencies
Make sure these are installed:
```powershell
pip install -q openai langchain langchain-openai langchain-community email-validator
```

## Key Points
- `src` directory contains all the source code
- Python must have `src` in its path to find modules like `core`, `api`, `ai`, etc.
- PYTHONPATH must be set BEFORE running python
- Working directory should be the `backend` folder
