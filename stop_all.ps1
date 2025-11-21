# Stop All Running Services
# This script helps you stop both backend and frontend services

Write-Host "=========================================" -ForegroundColor Red
Write-Host "  Stopping Mini Legal Analyst Services" -ForegroundColor Red
Write-Host "=========================================" -ForegroundColor Red
Write-Host ""

# Find and stop Python processes running uvicorn (backend)
Write-Host "Stopping Backend Server..." -ForegroundColor Yellow
$backendProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*uvicorn*"
}

if ($backendProcesses) {
    $backendProcesses | ForEach-Object {
        Stop-Process -Id $_.Id -Force
        Write-Host "  ✓ Stopped backend process (PID: $($_.Id))" -ForegroundColor Green
    }
} else {
    Write-Host "  No backend processes found" -ForegroundColor Gray
}

# Find and stop Python processes running streamlit (frontend)
Write-Host "Stopping Frontend UI..." -ForegroundColor Yellow
$frontendProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*streamlit*"
}

if ($frontendProcesses) {
    $frontendProcesses | ForEach-Object {
        Stop-Process -Id $_.Id -Force
        Write-Host "  ✓ Stopped frontend process (PID: $($_.Id))" -ForegroundColor Green
    }
} else {
    Write-Host "  No frontend processes found" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "  All services stopped!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to close this window"
