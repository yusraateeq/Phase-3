#!/usr/bin/env python
"""
FOOLPROOF BACKEND STARTER
This sets PYTHONPATH in every possible way before doing anything else.
"""
import sys
import os
from pathlib import Path

# Method 1: Add to sys.path immediately
backend_dir = Path(__file__).parent.resolve()
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

# Method 2: Set environment variable
os.environ["PYTHONPATH"] = f"{src_dir}{os.pathsep}{os.environ.get('PYTHONPATH', '')}"

# Method 3: Change to backend directory
os.chdir(str(backend_dir))

# NOW safe to import
if __name__ == "__main__":
    import uvicorn
    
    print(f"\n{'='*70}")
    print("BACKEND SERVER - STARTING")
    print(f"{'='*70}")
    print(f"Backend: {backend_dir}")
    print(f"Src: {src_dir}")
    print(f"PYTHONPATH: {sys.path[0]}")
    print(f"CWD: {os.getcwd()}")
    
    # Import and show config
    from core.config import settings
    print(f"\nServer Config:")
    print(f"  Host: {settings.HOST}")
    print(f"  Port: {settings.PORT}")
    print(f"  Debug: {settings.DEBUG}")
    print(f"  OpenAI Model: {settings.OPENAI_MODEL}")
    
    print(f"\n{'='*70}")
    print(f"Starting Uvicorn...\n")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
