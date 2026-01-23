"""
Site customization - runs automatically when Python starts.
This ensures the backend src directory is always in the path.
This is critical for ensuring PYTHONPATH persists even on module reloads.
"""
import sys
import os
from pathlib import Path

# This will run even if Python is invoked from anywhere
# Find the backend src directory relative to common patterns
try:
    # Try to find src directory from current working directory
    cwd = Path.cwd()
    possible_paths = [
        cwd / "src",                    # If running from backend dir
        cwd.parent / "backend" / "src", # If running from Phase-3
        cwd / "backend" / "src",        # If running from Phase-3/Phase-3
        Path(__file__).parent / "src",  # Relative to this file's location
    ]
    
    for src_path in possible_paths:
        if src_path.exists() and (src_path / "core").exists():
            src_path_str = str(src_path.resolve())
            if src_path_str not in sys.path:
                sys.path.insert(0, src_path_str)
            # Also set environment variable for subprocesses
            os.environ.setdefault("PYTHONPATH", src_path_str)
            break
except Exception:
    pass
