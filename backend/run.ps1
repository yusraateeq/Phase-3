# PowerShell Script to Run Backend Correctly

# Get to the backend directory
Set-Location "\\wsl.localhost\Ubuntu-24.04\home\yusraa\Phase-3\Phase-3\backend"

# Set PYTHONPATH to include src directory
$env:PYTHONPATH = "${PWD}\src;$env:PYTHONPATH"

Write-Host "Starting Backend Server"
Write-Host "======================="
Write-Host "Backend Path: $(Get-Location)"
Write-Host "PYTHONPATH: $env:PYTHONPATH"
Write-Host ""

# Run uvicorn with PYTHONPATH set
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
