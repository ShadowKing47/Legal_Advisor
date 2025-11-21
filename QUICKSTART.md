# Quick Start Guide

## 🚀 Starting the Application

### Option 1: Start Everything at Once (Recommended)
Run this single command to start both backend and frontend:

```powershell
.\start_all.ps1
```

This will:
- Open two new PowerShell windows (one for backend, one for frontend)
- Start the backend API on http://localhost:8000
- Start the frontend UI on http://localhost:8501
- Automatically open your browser to the Streamlit interface

### Option 2: Start Services Individually
If you prefer to start services separately:

**Backend:**
```powershell
.\start_backend.ps1
```

**Frontend:**
```powershell
.\start_frontend.ps1
```

## 🛑 Stopping the Application

### Option 1: Use the Stop Script
```powershell
.\stop_all.ps1
```

### Option 2: Manual Stop
- Press `CTRL+C` in each PowerShell window
- Or simply close the PowerShell windows

## 📍 Service URLs

- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Redoc**: http://localhost:8000/redoc

## ⚙️ Prerequisites

Before running, ensure:
1. Virtual environment is created: `python -m venv venv`
2. Dependencies are installed: `pip install -r requirements.txt`
3. `.env` file exists with your `GROQ_API_KEY`

## 📝 Available Scripts

| Script | Description |
|--------|-------------|
| `start_all.ps1` | Start both backend and frontend simultaneously |
| `start_backend.ps1` | Start only the backend API server |
| `start_frontend.ps1` | Start only the frontend Streamlit UI |
| `stop_all.ps1` | Stop all running services |

## 🔧 Troubleshooting

**Port already in use?**
- Run `.\stop_all.ps1` to stop any existing services
- Or manually kill processes using ports 8000 and 8501

**Virtual environment not activating?**
- Ensure you're running PowerShell (not CMD)
- Check execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Backend not connecting?**
- Verify `.env` file exists in both root and `backend/` directories
- Check that `GROQ_API_KEY` is set correctly

For more detailed troubleshooting, see `TROUBLESHOOTING.md`.
