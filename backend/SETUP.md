# Backend Setup and Running Guide

## Installation

### 1. Create Virtual Environment (if not already created)
```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**On Linux/WSL:**
```bash
source venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**On Windows (cmd):**
```cmd
venv\Scripts\activate.bat
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

If you encounter the "No module named 'openai'" error, install AI dependencies explicitly:
```bash
pip install openai langchain langchain-openai langchain-community
```

## Running the Backend

### Option 1: Using the Python Startup Script (Recommended)
```bash
python run.py
```

This automatically:
- Sets up the Python path correctly
- Verifies all imports work
- Starts the server with proper configuration

### Option 2: Using Uvicorn Directly with PYTHONPATH
**On Linux/WSL:**
```bash
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
cd src
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**On Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "${PWD}/src;$env:PYTHONPATH"
cd src
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Using the Shell Script (Linux/WSL)
```bash
chmod +x run.sh
./run.sh
```

## Troubleshooting

### "No module named 'openai'" Error
This occurs when the Python path isn't set up correctly. Solutions:

1. **Use run.py** (recommended):
   ```bash
   python run.py
   ```

2. **Set PYTHONPATH before running**:
   ```bash
   export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. **Install packages to global environment**:
   ```bash
   pip install openai langchain langchain-openai langchain-community
   ```

### Database Connection Error
Ensure the `.env` file is properly configured with:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### CORS Errors
The backend is configured to accept requests from `localhost` and `127.0.0.1` on any port. Update the `allow_origin_regex` in `main.py` if needed.

## API Endpoints

- **Health Check**: `GET /health` or `GET /`
- **Chat**: `POST /api/chat`
- **Authentication**: `/api/auth/...`
- **Tasks**: `/api/tasks/...`
- **API Docs**: `GET /docs` (Swagger UI)
- **API Redoc**: `GET /redoc` (ReDoc)

## Environment Variables

See `.env` file for configuration:
- `DEBUG`: Enable debug mode (default: false)
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for AI features
- `OPENAI_API_BASE`: API base URL (supports other providers)
- `OPENAI_MODEL`: Default model to use

## Development

### Running Tests
```bash
pytest
```

### Code Structure
```
backend/
├── src/
│   ├── api/          # API route handlers
│   ├── ai/           # AI agent and MCP server
│   ├── core/         # Core configuration and database
│   ├── middleware/   # FastAPI middleware
│   ├── models/       # SQLModel database models
│   └── main.py       # FastAPI app entry point
├── run.py           # Startup script
└── requirements.txt # Python dependencies
```

## Notes

- The application requires Python 3.11+
- PostgreSQL database is required
- OpenAI API key is required for AI features
- All imports are relative to the `src` directory
