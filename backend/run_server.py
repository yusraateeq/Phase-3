#!/usr/bin/env python
"""
MUST USE THIS TO RUN THE BACKEND - Direct, foolproof startup.
This sets PYTHONPATH in the environment and runs uvicorn correctly.
Usage: python -u run_server.py
"""
import subprocess
import sys
import os
from pathlib import Path

# Get paths
backend_dir = Path(__file__).parent.resolve()
src_dir = backend_dir / "src"

# Set environment variable BEFORE spawning subprocess
env = os.environ.copy()
env["PYTHONPATH"] = f"{src_dir}{os.pathsep}{env.get('PYTHONPATH', '')}"

# Also set it in this process (for testing)
sys.path.insert(0, str(src_dir))

print("\n" + "="*70)
print("BACKEND STARTUP")
print("="*70)
print(f"Backend directory: {backend_dir}")
print(f"Source directory: {src_dir}")
print(f"PYTHONPATH set to: {env['PYTHONPATH'][:80]}...")

# Validate imports work in this process
print("\nValidating imports...")
try:
    import openai
    print(f"  ✓ OpenAI {openai.__version__}")
    
    from core.config import settings
    print(f"  ✓ Config loaded - {settings.APP_NAME}")
    
    from ai.smart_agent import SmartAgent
    print(f"  ✓ SmartAgent ready")
    
    print("\n✓ All imports validated!")
    
except ImportError as e:
    print(f"  ✗ Import failed: {e}")
    print("\nFix: Run this first:")
    print("  pip install openai langchain langchain-openai langchain-community")
    sys.exit(1)

print("="*70)
print(f"Starting server on {settings.HOST}:{settings.PORT}")
print(f"Debug: {settings.DEBUG}")
print(f"API Docs: http://localhost:{settings.PORT}/docs")
print("="*70 + "\n")

# Change to backend directory
os.chdir(str(backend_dir))

# Run uvicorn with PYTHONPATH set
try:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            f"--host={settings.HOST}",
            f"--port={settings.PORT}",
            "--reload" if settings.DEBUG else "",
        ],
        env=env,
        check=False,
    )
except KeyboardInterrupt:
    print("\n\nServer stopped.")
    sys.exit(0)
