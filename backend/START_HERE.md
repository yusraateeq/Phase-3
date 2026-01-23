# ✓ BACKEND RUNNING INSTRUCTIONS - READ THIS

## The Problem Was
Your computer uses **Windows Python** but accesses backend files via **WSL paths** (`\\wsl.localhost\...`). When running the backend without setting PYTHONPATH, Python can't find the `src` directory where all the code lives, causing:
```
No module named 'openai'
No module named 'core'
No module named 'api'
etc...
```

## The Solution

### EASIEST: Run the Python startup script
```powershell
cd "\\wsl.localhost\Ubuntu-24.04\home\yusraa\Phase-3\Phase-3\backend"
python run_backend.py
```

This script:
- ✓ Sets Python path automatically
- ✓ Verifies all imports work
- ✓ Starts the server with proper configuration
- ✓ Shows clear error messages if something fails

### ALTERNATIVE 1: Manual PYTHONPATH setup (PowerShell)
```powershell
cd "\\wsl.localhost\Ubuntu-24.04\home\yusraa\Phase-3\Phase-3\backend"
$env:PYTHONPATH = "${PWD}\src;$env:PYTHONPATH"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### ALTERNATIVE 2: Use the batch file (CMD)
```cmd
cd "\\wsl.localhost\Ubuntu-24.04\home\yusraa\Phase-3\Phase-3\backend"
run.bat
```

## Verify It Works

Once the backend is running, test the health endpoint:
```powershell
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "app": "Todo Backend API",
  "version": "3.0.0",
  "debug": true
}
```

## Required Packages

Make sure all dependencies are installed:
```powershell
pip install -q openai langchain langchain-openai langchain-community email-validator
```

If you get any "No module named..." errors, run the above command.

## API Documentation

Once running, visit:
- **API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"
**Solution**: Install missing packages
```powershell
pip install openai langchain langchain-openai langchain-community
```

### "No module named 'core' / 'api' / etc"
**Solution**: PYTHONPATH is not set. Use one of the methods above.

### Port 8000 already in use
**Solution**: Kill the process or use a different port
```powershell
# Kill on port 8000
netstat -ano | findstr :8000  # Find PID
taskkill /PID <PID> /F       # Kill process

# Or use different port
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

### Still getting import errors
**Solution**: Verify you're in the right directory and run the startup script:
```powershell
cd "\\wsl.localhost\Ubuntu-24.04\home\yusraa\Phase-3\Phase-3\backend"
python run_backend.py
```

## How It Works

1. **run_backend.py** is executed
2. It adds `src` directory to Python's path
3. It validates all imports work
4. It starts uvicorn with proper configuration
5. uvicorn loads main.py from the backend directory
6. main.py can now import from `core`, `api`, `ai` modules because they're in path

## Files Reference

- `backend/run_backend.py` - **Use this to run the backend**
- `backend/run.bat` - Windows batch alternative
- `backend/run.sh` - Linux/WSL shell alternative  
- `backend/run.ps1` - PowerShell alternative
- `backend/main.py` - FastAPI app entry point
- `backend/src/` - All source code (api, core, ai, etc)

## Key Takeaway

**Always use one of these methods to start the backend:**
1. `python run_backend.py` ← RECOMMENDED
2. Set `$env:PYTHONPATH` before running uvicorn
3. Use `run.bat` or `run.ps1` scripts

Do NOT run uvicorn directly without setting PYTHONPATH!
