"""
Diagnostic script - Run this to see exactly what's wrong
Usage: python diagnose.py
"""
import sys
import os
import subprocess
from pathlib import Path

print("\n" + "="*70)
print("BACKEND DIAGNOSTIC TOOL")
print("="*70)

backend_dir = Path.cwd()
src_dir = backend_dir / "src"

print(f"\n1. CHECKING DIRECTORY STRUCTURE")
print(f"   Backend: {backend_dir}")
print(f"   Src: {src_dir}")
print(f"   Exists: {src_dir.exists()}")

if not src_dir.exists():
    print("   ERROR: src directory not found!")
    sys.exit(1)

print(f"\n2. CHECKING REQUIRED FILES")
files_to_check = [
    ("main.py", backend_dir / "main.py"),
    ("core/config.py", src_dir / "core" / "config.py"),
    ("api/chat.py", src_dir / "api" / "chat.py"),
    ("ai/smart_agent.py", src_dir / "ai" / "smart_agent.py"),
    ("requirements.txt", backend_dir / "requirements.txt"),
]

all_exist = True
for name, path in files_to_check:
    exists = path.exists()
    status = "✓" if exists else "✗"
    print(f"   {status} {name}")
    if not exists:
        all_exist = False

if not all_exist:
    print("   ERROR: Some files are missing!")
    sys.exit(1)

print(f"\n3. CHECKING PYTHON PACKAGES")
sys.path.insert(0, str(src_dir))

packages = ["openai", "fastapi", "sqlmodel", "pydantic"]
all_installed = True

for pkg in packages:
    try:
        __import__(pkg)
        print(f"   ✓ {pkg}")
    except ImportError:
        print(f"   ✗ {pkg} NOT INSTALLED")
        all_installed = False

if not all_installed:
    print("\n   FIX: Run: pip install -r requirements.txt")
    sys.exit(1)

print(f"\n4. CHECKING BACKEND IMPORTS")
try:
    from core.config import settings
    print(f"   ✓ core.config")
    
    from ai.smart_agent import SmartAgent
    print(f"   ✓ ai.smart_agent")
    
    from api import chat
    print(f"   ✓ api.chat")
    
    print(f"   ✓ All core imports successful!")
except ImportError as e:
    print(f"   ✗ Import failed: {e}")
    sys.exit(1)

print(f"\n5. CHECKING IF SERVER IS RUNNING")
try:
    import urllib.request
    response = urllib.request.urlopen("http://localhost:8000/health", timeout=2)
    print(f"   ✓ Server IS running on port 8000")
except Exception as e:
    print(f"   ✗ Server NOT responding on port 8000")
    print(f"      Error: {e}")
    print(f"\n   FIX: Start the backend with one of these commands:")
    print(f"        PowerShell: cd backend; $env:PYTHONPATH=\"${{PWD}}\\src\"; python -m uvicorn main:app --host 0.0.0.0 --port 8000")
    print(f"        CMD: cd backend & set PYTHONPATH=%CD%\\src & python -m uvicorn main:app --host 0.0.0.0 --port 8000")
    print(f"        Or run: START_BACKEND.bat")

print(f"\n6. ENVIRONMENT CHECK")
print(f"   Current directory: {os.getcwd()}")
print(f"   Python: {sys.executable}")
print(f"   Python version: {sys.version.split()[0]}")

print(f"\n" + "="*70)
print("DIAGNOSTIC COMPLETE")
print("="*70 + "\n")
