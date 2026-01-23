# Running the Backend - Complete Reference

## Are You Using Docker?

### YES - Using Docker
```powershell
cd backend
docker compose up
```

**Note**: I've fixed the Dockerfile. Rebuild it:
```powershell
docker compose up --build
```

### NO - Running Locally on Windows

**Use this command:**
```powershell
cd backend
python run_backend.py
```

Or manually set PYTHONPATH:
```powershell
$env:PYTHONPATH = "${PWD}\src;$env:PYTHONPATH"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## What I Fixed

### Local Development (Windows)
- ✅ Created `run_backend.py` - sets up PYTHONPATH before starting server
- ✅ Enhanced `main.py` - adds src to path on import
- ✅ Updated `WINDOWS_SETUP.md` - Windows-specific instructions

### Docker Deployment
- ✅ Fixed `Dockerfile` - sets PYTHONPATH environment variable
- ✅ Added `requirements.txt` usage (instead of pyproject.toml)
- ✅ Ensures /app/src is in path when container runs

## Test It's Working

### Local (Windows)
```powershell
curl http://localhost:8000/health
```

### Docker
```powershell
docker compose up
# Then in another terminal:
curl http://localhost:8000/health
```

## Error Checklist

If you still get "No module named 'openai'":

1. **Local development?** → Use `python run_backend.py`
2. **Using Docker?** → Run `docker compose up --build` to rebuild
3. **Still failing?** → Check: `pip install -r requirements.txt`

## Files Changed

- `Dockerfile` ← **UPDATED** - Now sets PYTHONPATH correctly
- `backend/run_backend.py` ← **NEW** - Use this to run locally
- `backend/main.py` ← **UPDATED** - Path setup improved

## Next Steps

1. **Identify your setup**: Docker or local?
2. **Run using correct method** (see above)
3. **Test**: `curl http://localhost:8000/health`
4. **If error**: Run `pip install -r requirements.txt`
