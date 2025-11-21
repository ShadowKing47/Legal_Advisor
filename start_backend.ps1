# Start Backend Server - UPDATED
# Run this from the mini-legal-analyst directory

Write-Host "Starting Mini Legal Analyst Backend..." -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Ensure .env exists in backend directory
if (-not (Test-Path "backend\.env")) {
    Write-Host "Copying .env to backend directory..." -ForegroundColor Yellow
    Copy-Item ".env" "backend\.env"
}

# Start FastAPI server from backend directory
Write-Host ""
Write-Host "Backend API starting at http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Documentation at http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Navigate to backend and run uvicorn
Set-Location backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
