#!/bin/bash
# Backend startup script with proper environment setup

set -e

# Get the directory where this script is located
BACKEND_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Add src to PYTHONPATH
export PYTHONPATH="${BACKEND_DIR}/src:${PYTHONPATH}"

# Activate virtual environment if it exists
if [ -d "${BACKEND_DIR}/venv" ]; then
    source "${BACKEND_DIR}/venv/bin/activate"
fi

# Change to backend directory
cd "${BACKEND_DIR}"

# Run the application
echo "Starting backend server..."
echo "PYTHONPATH: $PYTHONPATH"
echo "Working directory: $(pwd)"

# Run with debug output
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
