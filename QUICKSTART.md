# Mini Legal Analyst - Quick Start Guide

## Quick Setup

1. **Activate Virtual Environment:**
   ```bash
   .\venv\Scripts\activate
   ```

2. **Install Dependencies (if not already done):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key:**
   - Ensure `.env` file exists with your Groq API key
   - The key is already configured if you followed the setup

## Running the System

### Option 1: Run Both Services (Recommended)

**Terminal 1 - Start Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start Frontend:**
```bash
streamlit run frontend/streamlit_app.py
```

### Option 2: Use PowerShell Scripts

**Start Backend:**
```powershell
.\start_backend.ps1
```

**Start Frontend:**
```powershell
.\start_frontend.ps1
```

## Access Points

- **Frontend UI:** http://localhost:8501
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## First Time Usage

1. Open the Streamlit UI at http://localhost:8501
2. Select "Full Report" mode in the sidebar
3. Upload a PDF document (e.g., Universal Credit Act 2025)
4. Click "Generate Full Report"
5. Wait 2-5 minutes for processing
6. View results and download JSON report

## Troubleshooting

**If backend fails to start:**
- Check that port 8000 is not in use
- Verify `.env` file contains GROQ_API_KEY
- Check virtual environment is activated

**If frontend fails to start:**
- Check that port 8501 is not in use
- Ensure backend is running first
- Verify all dependencies are installed

**If analysis fails:**
- Check Groq API key is valid
- Ensure PDF is readable (not scanned image)
- Check backend logs for errors

## Testing the System

### Quick Test
1. Use a small PDF (5-10 pages)
2. Run "Quick Analysis" mode
3. Test each step individually

### Full Test
1. Use a complete legal document
2. Run "Full Report" mode
3. Verify all 6 categories are extracted
4. Check all 6 rules are validated
5. Download and inspect JSON report

## System Architecture

```
User → Streamlit UI → FastAPI → Core Modules → Groq API
                                    ↓
                              FAISS Vector Store
```

## Next Steps

- Review the generated JSON reports in `data/reports/`
- Explore the API documentation at http://localhost:8000/docs
- Customize settings in `backend/app/config.py`
- Add your own legal documents for analysis

---

For detailed documentation, see README.md
