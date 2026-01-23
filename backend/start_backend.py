#!/usr/bin/env python
"""
Simple backend startup - Works with Windows/WSL paths
Just: python start_backend.py
"""
import sys
import os
from pathlib import Path

# Setup paths first
backend_dir = Path(__file__).parent.resolve()
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))
os.chdir(str(backend_dir))

# Now import everything
print("\n" + "="*70)
print("STARTING TODO BACKEND")
print("="*70)
print(f"Backend: {backend_dir}")
print(f"Python: {sys.executable}")

# Lazy imports to avoid multiprocessing issues
import uvicorn
from core.config import settings

print(f"\nStarting server on {settings.HOST}:{settings.PORT}")
print(f"Debug mode: {settings.DEBUG}")
print(f"API Docs: http://localhost:{settings.PORT}/docs\n")

# Run the server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
