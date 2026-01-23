"""
Pytest configuration and path setup.
This file is loaded automatically by pytest and other tools.
"""
import sys
from pathlib import Path

# Add src to path for all imports
backend_dir = Path(__file__).parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))
