#!/usr/bin/env python
"""
Backend startup script that properly sets PYTHONPATH as environment variable.
This ensures PYTHONPATH persists through module reloads and subprocess calls.
"""
import sys
import os
import subprocess
from pathlib import Path

def main():
    backend_dir = Path(__file__).parent.resolve()
    src_dir = backend_dir / "src"
    
    # Create environment with PYTHONPATH set
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{src_dir}{os.pathsep}{env.get('PYTHONPATH', '')}"
    
    print(f"\n{'='*70}")
    print("BACKEND SERVER - STARTING WITH PYTHONPATH")
    print(f"{'='*70}")
    print(f"Backend Dir: {backend_dir}")
    print(f"Src Dir: {src_dir}")
    print(f"PYTHONPATH: {env['PYTHONPATH']}")
    print(f"{'='*70}\n")
    
    # Use subprocess to ensure PYTHONPATH is inherited by child process
    cmd = [
        sys.executable,
        "-m", "uvicorn",
        "main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload",
    ]
    
    try:
        # Start uvicorn in subprocess with proper environment
        subprocess.run(
            cmd,
            cwd=str(backend_dir),
            env=env,
            check=False
        )
    except KeyboardInterrupt:
        print("\n\nBackend stopped by user")
    except Exception as e:
        print(f"\nError starting backend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
