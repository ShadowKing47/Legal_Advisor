# Installation Guide - Mini Legal Analyst System

Complete installation instructions for the Mini Legal Analyst System with premium glassmorphism UI.

## 📋 Prerequisites

- **Python 3.8+** (tested on Python 3.13)
- **Windows PowerShell** (for startup scripts)
- **Groq API Key** (free tier available)
- **4GB RAM minimum** (8GB recommended)
- **Internet connection** (for API calls)

## 🚀 Quick Installation

### Step 1: Get Groq API Key

1. Visit https://console.groq.com
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `gsk_`)

### Step 2: Setup Project

```powershell
# Navigate to project directory
cd mini-legal-analyst

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment

```powershell
# Create .env file
copy .env.example .env

# Edit .env file and add your API key
notepad .env
```

Add this line to `.env`:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

**Important:** Make sure the `.env` file is saved as UTF-8 without BOM.

### Step 4: Start the System

```powershell
# Start both backend and frontend
.\start_all.ps1
```

This will:
- Activate the virtual environment
- Start backend at http://localhost:8000
- Start frontend at http://localhost:8501
- Open the UI in your browser

## 📦 Dependencies

The system requires these Python packages:

### Core Web Framework
- `fastapi` - Backend API framework
- `uvicorn[standard]` - ASGI server
- `pydantic` - Data validation
- `pydantic-settings` - Settings management
- `python-dotenv` - Environment variables

### UI and Utilities
- `streamlit` - Frontend UI framework
- `requests` - HTTP client
- `pdfplumber` - PDF text extraction

### LangChain and AI
- `langchain` - LLM framework
- `langchain-community` - Community integrations
- `langchain-groq` - Groq LLM integration

### Vector Store and Embeddings
- `faiss-cpu` - Vector similarity search
- `sentence-transformers` - Text embeddings
- `tiktoken` - Token counting
- `numpy` - Numerical operations

## 🔧 Manual Installation (If Automatic Fails)

If `pip install -r requirements.txt` fails, install in groups:

```powershell
# Group 1: Core web framework
pip install fastapi uvicorn[standard] pydantic pydantic-settings python-dotenv

# Group 2: UI and utilities
pip install streamlit requests pdfplumber

# Group 3: LangChain and AI
pip install langchain langchain-community langchain-groq

# Group 4: Vector store and embeddings
pip install faiss-cpu sentence-transformers tiktoken numpy
```

## ✅ Verify Installation

### Check Installed Packages

```powershell
# List key packages
pip list | Select-String "fastapi|streamlit|langchain|faiss"
```

### Test API Key

```powershell
# Run the API key validator
python test_key.py
```

Expected output:
```
✅ VALID! Found 20 models
```

### Test Backend

```powershell
# Start backend
.\start_backend.ps1

# In another terminal, test health endpoint
curl http://localhost:8000/health
```

Expected output:
```json
{"status":"healthy"}
```

## 🎯 Startup Scripts

### `start_all.ps1` (Recommended)
Starts both backend and frontend in separate windows.

```powershell
.\start_all.ps1
```

### `start_backend.ps1`
Starts only the backend API server.

```powershell
.\start_backend.ps1
```

### `start_frontend.ps1`
Starts only the Streamlit UI.

```powershell
.\start_frontend.ps1
```

### `stop_all.ps1`
Stops all running Python processes.

```powershell
.\stop_all.ps1
```

### `restart_services.ps1`
Restarts both services (useful after updating `.env`).

```powershell
.\restart_services.ps1
```

## 🔑 API Key Management

### Update API Key

If you need to change your API key:

```powershell
# Option 1: Use the update script
python update_api_key.py

# Option 2: Edit .env manually
notepad .env
# Then restart: .\restart_services.ps1
```

### Validate API Key

```powershell
# Test if your key is valid
python test_key.py
```

### Fix BOM Issues

If you get `UnicodeDecodeError`:

```powershell
# Fix encoding issues
python update_api_key.py

# Verify fix
python verify_env.py
```

## 🌐 Access Points

After successful installation:

- **Frontend UI:** http://localhost:8501
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError`

**Solution:**
```powershell
# Ensure venv is activated
.\venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: `GROQ_API_KEY not found`

**Solution:**
1. Check `.env` file exists in project root
2. Verify it contains: `GROQ_API_KEY=your_key_here`
3. Restart backend: `.\restart_services.ps1`

### Issue: `401 Invalid API Key`

**Solution:**
1. Verify key at https://console.groq.com
2. Update `.env` with valid key
3. Run `.\restart_services.ps1`

### Issue: `UnicodeDecodeError`

**Solution:**
```powershell
# Fix BOM encoding issue
python update_api_key.py
```

### Issue: Port Already in Use

**Solution:**
```powershell
# Stop all services
.\stop_all.ps1

# Start fresh
.\start_all.ps1
```

### Issue: Frontend Can't Connect to Backend

**Solution:**
1. Verify backend is running: http://localhost:8000/health
2. Check firewall settings
3. Restart both services: `.\restart_services.ps1`

## 📁 Directory Structure After Installation

```
mini-legal-analyst/
├── venv/                    # Virtual environment
├── backend/
│   ├── app/
│   └── core/
├── frontend/
│   └── streamlit_app.py
├── data/
│   ├── uploads/             # Created automatically
│   ├── vector_store/        # Created automatically
│   └── reports/             # Created automatically
├── .env                     # Your API key (not in git)
├── .env.example
├── requirements.txt
└── start_all.ps1
```

## 🎨 UI Features Available

After installation, you'll have access to:

- ✨ Premium dark-theme glassmorphism UI
- 🎬 Cinematic gradient hero banner
- 💎 Frosted-glass cards with blur effects
- ⚡ Neon-accented headers
- 📊 Animated gradient progress bars
- 🏷️ Glowing PASS/FAIL badges
- 💻 VS Code-style JSON viewer
- 📥 Download JSON buttons

## 🔄 Updating the System

### Update Dependencies

```powershell
# Activate venv
.\venv\Scripts\activate

# Update packages
pip install --upgrade -r requirements.txt
```

### Update API Key

```powershell
# Use update script
python update_api_key.py

# Restart services
.\restart_services.ps1
```

## 📚 Next Steps

After installation:

1. **Read the README:** [README.md](README.md)
2. **Quick Start:** [QUICKSTART.md](QUICKSTART.md)
3. **Try the UI:** http://localhost:8501
4. **Explore API:** http://localhost:8000/docs

## 💡 Tips

- Always activate the virtual environment before running commands
- Use `start_all.ps1` for easiest startup
- Check API docs at http://localhost:8000/docs for endpoint details
- Use `stop_all.ps1` before closing terminals to clean up processes
- Run `test_key.py` if you encounter API key issues

## 🎓 Learning Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Streamlit Docs:** https://docs.streamlit.io
- **Groq API:** https://console.groq.com/docs
- **LangChain:** https://python.langchain.com

---

**Installation complete! Start analyzing legal documents with premium UI! 🎉**
