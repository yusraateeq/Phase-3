#!/usr/bin/env python
"""
Startup script for the Todo Backend API.
Sets up the Python path and environment before running the server.
"""
import sys
import os
from pathlib import Path

# Add src directory to Python path
backend_dir = Path(__file__).parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

# Verify imports work
try:
    import openai
    print(f"✓ OpenAI module found (version {openai.__version__})")
except ImportError as e:
    print(f"✗ Failed to import openai: {e}")
    sys.exit(1)

try:
    from core.config import settings
    print(f"✓ Core config loaded")
except ImportError as e:
    print(f"✗ Failed to import core.config: {e}")
    sys.exit(1)

# Run uvicorn
if __name__ == "__main__":
    import uvicorn
    
    print(f"\n{'='*60}")
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"Database: {settings.DATABASE_URL}")
    print(f"{'='*60}\n")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning",
    )
