# Restart Backend and Frontend
# This script stops all Python processes and starts fresh

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Restarting Mini Legal Analyst Services" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Stop all Python processes
Write-Host "Stopping all Python processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

# Start Backend
Write-Host "Starting Backend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\start_backend.ps1"
Start-Sleep -Seconds 5

# Start Frontend
Write-Host "Starting Frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\start_frontend.ps1"

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  Services Restarted!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Check the new terminal windows for status." -ForegroundColor Yellow
Write-Host ""
