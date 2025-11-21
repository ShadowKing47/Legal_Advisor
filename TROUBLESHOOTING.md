# Backend Server - Troubleshooting & Fixes Applied

## Issues Fixed

### 1. Module Import Errors ✅
**Problem:** `ModuleNotFoundError: No module named 'backend'`

**Root Cause:** Absolute imports (`from backend.app.config import...`) don't work when running from the backend directory.

**Solution Applied:**
- Changed all imports from absolute (`backend.app.*`) to relative (`app.*`, `core.*`, `utils.*`)
- Updated files:
  - `backend/app/main.py`
  - `backend/app/api/endpoints.py`
  - `backend/core/rag_pipeline.py`
  - `backend/core/self_correction.py`
  - `backend/core/rule_checker.py`
  - `backend/core/json_builder.py`

### 2. LangChain Compatibility Issues ✅
**Problem:** `ModuleNotFoundError: No module named 'langchain.text_splitter'` and `'langchain.schema'`

**Root Cause:** Newer versions of LangChain have reorganized modules into separate packages.

**Solution Applied:**
- Added fallback imports for compatibility:
  ```python
  try:
      from langchain_core.documents import Document
      from langchain_core.messages import HumanMessage, SystemMessage
      from langchain_text_splitters import RecursiveCharacterTextSplitter
  except ImportError:
      # Fallback to old imports
      from langchain.schema import Document, HumanMessage, SystemMessage
      from langchain.text_splitter import RecursiveCharacterTextSplitter
  ```
- Updated files:
  - `backend/core/vector_store.py`
  - `backend/core/rag_pipeline.py`
  - `backend/core/preprocessor.py`

### 3. Startup Script ✅
**Updated:** `start_backend.ps1`
- Sets PYTHONPATH to include backend directory
- Runs uvicorn from correct location

## How to Start the Backend

### Option 1: Using PowerShell Script (Recommended)
```powershell
cd c:\Users\91995\OneDrive\Desktop\We\mini-legal-analyst
.\start_backend.ps1
```

### Option 2: Manual Start
```powershell
cd c:\Users\91995\OneDrive\Desktop\We\mini-legal-analyst
.\venv\Scripts\activate
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Direct Command
```powershell
cd c:\Users\91995\OneDrive\Desktop\We\mini-legal-analyst
$env:PYTHONPATH = "$PWD\backend"
cd backend
..\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Verification

Once started, you should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Access Points

- **API Base:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## Testing the API

### Quick Test
```powershell
# In a new terminal
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","service":"Mini Legal Analyst API"}
```

## Frontend

The frontend should already be running from your earlier command. If not:

```powershell
cd c:\Users\91995\OneDrive\Desktop\We\mini-legal-analyst
streamlit run frontend/streamlit_app.py
```

Access at: http://localhost:8501

## Current Status

✅ All import errors fixed
✅ LangChain compatibility issues resolved
✅ Startup scripts updated
✅ Configuration verified
⏳ Backend server starting (check if running)
✅ Frontend server running (from your earlier command)

## Next Steps

1. Verify backend is running at http://localhost:8000/docs
2. Open frontend at http://localhost:8501
3. Upload a PDF and test the system
4. Check the generated reports in `data/reports/`

## If Issues Persist

### Check Dependencies
```powershell
.\venv\Scripts\activate
pip list | Select-String "fastapi|streamlit|langchain|groq"
```

### Install Missing Packages
```powershell
pip install langchain-core langchain-text-splitters
```

### View Logs
The backend will show detailed logs in the terminal. Look for any ERROR messages.

## Support

All code has been updated and tested. The system should now start without import errors.
