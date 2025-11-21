# Start Frontend (Streamlit)
# Run this from the mini-legal-analyst directory

Write-Host "Starting Mini Legal Analyst Frontend..." -ForegroundColor Green

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Start Streamlit
Write-Host "Frontend UI starting at http://localhost:8501" -ForegroundColor Cyan

streamlit run frontend/streamlit_app.py
