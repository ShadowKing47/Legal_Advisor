# Start Both Backend and Frontend Simultaneously
# Run this from the mini-legal-analyst directory

Write-Host "=========================================" -ForegroundColor Green
Write-Host "  Mini Legal Analyst - Full System Start" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env file not found!" -ForegroundColor Red
    Write-Host "Please copy .env.example to .env and configure your API keys." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Ensure .env exists in backend directory
if (-not (Test-Path "backend\.env")) {
    Write-Host "Copying .env to backend directory..." -ForegroundColor Yellow
    Copy-Item ".env" "backend\.env"
}

Write-Host ""
Write-Host "Starting services..." -ForegroundColor Cyan
Write-Host "  - Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "  - API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  - Frontend UI: http://localhost:8501" -ForegroundColor White
Write-Host ""
Write-Host "Press CTRL+C to stop all services" -ForegroundColor Yellow
Write-Host ""

# Start backend in a new PowerShell window
Write-Host "[1/2] Starting Backend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\start_backend.ps1"

# Wait a moment for backend to initialize
Write-Host "Waiting 3 seconds for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start frontend in a new PowerShell window
Write-Host "[2/2] Starting Frontend UI..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\start_frontend.ps1"

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "  Both services are starting!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Two new PowerShell windows have opened:" -ForegroundColor Cyan
Write-Host "  1. Backend Server (FastAPI)" -ForegroundColor White
Write-Host "  2. Frontend UI (Streamlit)" -ForegroundColor White
Write-Host ""
Write-Host "To stop the services:" -ForegroundColor Yellow
Write-Host "  - Press CTRL+C in each window, or" -ForegroundColor White
Write-Host "  - Close both PowerShell windows" -ForegroundColor White
Write-Host ""
Write-Host "The frontend will open automatically in your browser." -ForegroundColor Cyan
Write-Host "If not, navigate to: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "This window can be closed safely." -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to close this window"
