# Installation Instructions

## Current Status

The virtual environment has been created and most dependencies are being installed.

## Complete Installation

If the automatic installation didn't complete, run these commands:

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

## Verify Installation

```bash
# Check if packages are installed
pip list | Select-String "fastapi|streamlit|langchain|faiss"
```

## Expected Packages

- fastapi
- uvicorn
- pydantic
- pydantic-settings
- python-dotenv
- streamlit
- requests
- pdfplumber
- langchain
- langchain-community
- langchain-groq
- faiss-cpu
- sentence-transformers
- tiktoken
- numpy

## If Installation Fails

Try installing in groups:

```bash
# Core web framework
pip install fastapi uvicorn[standard] pydantic pydantic-settings python-dotenv

# UI and utilities
pip install streamlit requests pdfplumber

# LangChain and AI
pip install langchain langchain-community langchain-groq

# Vector store and embeddings
pip install faiss-cpu sentence-transformers tiktoken numpy
```

## Next Steps After Installation

1. Verify `.env` file contains your Groq API key
2. Start the backend: `.\start_backend.ps1`
3. Start the frontend: `.\start_frontend.ps1`
4. Access UI at http://localhost:8501
