# HOW TO RUN BACKEND - DEFINITIVE GUIDE

## The Problem
When you run the backend server, it fails with:
```
No module named 'openai'
```

This happens when you don't set PYTHONPATH before starting Python.

## Why It Happens
```
python -m uvicorn main:app                    ← FAILS (no PYTHONPATH set)
python run_backend.py                         ← WORKS (sets PYTHONPATH internally)
```

## MUST DO ONE OF THESE:

### ✓ METHOD 1: Use the Startup Script (EASIEST)
```powershell
cd "\\wsl.localhost\Ubuntu-24.04\home\yusraa\Phase-3\Phase-3\backend"
python run_backend.py
```

Done. It works. No other steps needed.

### ✓ METHOD 2: Set PYTHONPATH First (PowerShell)
```powershell
cd "\\wsl.localhost\Ubuntu-24.04\home\yusraa\Phase-3\Phase-3\backend"
$env:PYTHONPATH = "${PWD}\src;$env:PYTHONPATH"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### ✓ METHOD 3: Use Batch File (CMD)
```cmd
cd "\\wsl.localhost\Ubuntu-24.04\home\yusraa\Phase-3\Phase-3\backend"
run.bat
```

### ✗ DON'T DO THIS (It Won't Work)
```powershell
python -m uvicorn main:app              ← Will fail with "No module named 'openai'"
```

## Test It's Working
Open another terminal and run:
```powershell
curl http://localhost:8000/health
```

Should return:
```json
{"status":"healthy","app":"Todo Backend API","version":"3.0.0","debug":true}
```

If you see JSON, the backend is working!

## Troubleshooting

If you still get "No module named 'openai'":

1. **Verify packages are installed:**
   ```powershell
   pip install openai langchain langchain-openai langchain-community email-validator
   ```

2. **Check you're in the right directory:**
   ```powershell
   cd "\\wsl.localhost\Ubuntu-24.04\home\yusraa\Phase-3\Phase-3\backend"
   pwd  # Should show the backend path
   ```

3. **Verify run_backend.py works:**
   ```powershell
   python -c "import sys; sys.path.insert(0, 'src'); from core.config import settings; print('OK')"
   ```

4. **Use the correct script:**
   - NOT: `python main.py`
   - NOT: `uvicorn main:app`
   - YES: `python run_backend.py` or set PYTHONPATH manually

## Summary

**Use this command to start the backend:**
```powershell
cd backend
python run_backend.py
```

That's it. Everything else is handled automatically.
