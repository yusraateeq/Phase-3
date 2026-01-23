#!/usr/bin/env python
"""
CRITICAL: This must be run from the backend directory.
Sets up the Python path BEFORE any imports, then runs the server.
Usage: python run_backend.py
"""
import sys
import os
from pathlib import Path

# Get the backend directory
backend_dir = Path(__file__).parent.resolve()
src_dir = backend_dir / "src"

# CRITICAL: Add src to path BEFORE any other imports
sys.path.insert(0, str(src_dir))
os.chdir(str(backend_dir))

# Set PYTHONPATH env var for subprocess calls
os.environ["PYTHONPATH"] = f"{src_dir}{os.pathsep}{os.environ.get('PYTHONPATH', '')}"

print(f"\n{'='*70}")
print(f"Backend Startup - Windows/WSL Compatible")
print(f"{'='*70}")
print(f"Backend directory: {backend_dir}")
print(f"Source directory: {src_dir}")
print(f"Python path[0]: {sys.path[0]}")
print(f"Working directory: {os.getcwd()}")
print(f"PYTHONPATH: {os.environ['PYTHONPATH'][:60]}...")

# Now verify imports work
print(f"\n{'Validating imports...'}")
errors = []
try:
    import openai
    print(f"  [OK] OpenAI ({openai.__version__})")
except ImportError as e:
    print(f"  [FAIL] OpenAI: {e}")
    errors.append(str(e))

try:
    from core.config import settings
    print(f"  [OK] Core config ({settings.APP_NAME})")
except ImportError as e:
    print(f"  [FAIL] Core config: {e}")
    errors.append(str(e))

try:
    from ai.smart_agent import SmartAgent
    print(f"  [OK] SmartAgent")
except ImportError as e:
    print(f"  [FAIL] SmartAgent: {e}")
    errors.append(str(e))

if errors:
    print(f"\n[FAIL] Import validation failed!")
    for error in errors:
        print(f"  - {error}")
    print(f"\nFix: Run 'pip install openai langchain langchain-openai langchain-community'")
    sys.exit(1)

print(f"\n[OK] All imports validated successfully!")
print(f"{'='*70}\n")

# Run uvicorn
if __name__ == "__main__":
    import uvicorn
    
    print(f"Starting server on {settings.HOST}:{settings.PORT}")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"Visit http://localhost:{settings.PORT}/docs for API docs\n")
    
    try:
        uvicorn.run(
            "main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
            log_level="info" if settings.DEBUG else "warning",
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        sys.exit(0)
