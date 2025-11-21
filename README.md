# Mini Legal Analyst System

A production-ready RAG-based legal document analysis system with self-correction capabilities, built using FastAPI, Streamlit, LangChain, and Llama 3.1 via Groq.

## 🎯 Overview

This system provides comprehensive analysis of legal documents through:
- **PDF Extraction** with intelligent text cleaning
- **Vector Search** using FAISS and HuggingFace embeddings
- **RAG Pipeline** powered by Llama 3.1 (via Groq)
- **Self-Correction Agent** with reflection loop for quality assurance
- **Rule Validation** against 6 key legal document requirements
- **Structured JSON Reports** with complete analysis results

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │  ← User Interface
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI API   │  ← REST Endpoints
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│         Core Modules                │
│  • PDF Extractor (pdfplumber)       │
│  • Preprocessor (LangChain)         │
│  • Vector Store (FAISS)             │
│  • RAG Pipeline (Groq + Llama 3.1)  │
│  • Self-Correction Agent            │
│  • Rule Checker                     │
│  • JSON Builder                     │
└─────────────────────────────────────┘
```

## 📁 Project Structure

```
mini-legal-analyst/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration management
│   │   ├── schemas.py           # Pydantic models
│   │   └── api/
│   │       └── endpoints.py     # API route handlers
│   ├── core/
│   │   ├── pdf_extractor.py     # PDF text extraction
│   │   ├── preprocessor.py      # Text chunking
│   │   ├── vector_store.py      # FAISS vector store
│   │   ├── rag_pipeline.py      # RAG with LLM
│   │   ├── self_correction.py   # Reflection loop
│   │   ├── rule_checker.py      # Legal rule validation
│   │   └── json_builder.py      # Report generation
│   └── utils/
│       └── helpers.py           # Utility functions
├── frontend/
│   └── streamlit_app.py         # Streamlit UI
├── data/
│   ├── uploads/                 # Uploaded PDFs
│   ├── vector_store/            # FAISS indices
│   └── reports/                 # Generated reports
├── .env                         # Environment variables (not in git)
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Groq API key (free tier available at https://console.groq.com)

### Setup Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd mini-legal-analyst
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   # Copy the example file
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac

   # Edit .env and add your Groq API key
   # GROQ_API_KEY=your_actual_api_key_here
   ```

## ⚙️ Configuration

The system uses environment variables for configuration. Key settings in `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Additional settings can be modified in `backend/app/config.py`:
- LLM model and parameters
- Chunk size and overlap
- Retrieval settings
- Self-correction thresholds

## 🎮 Usage

### Starting the Backend (FastAPI)

```bash
# From project root
cd mini-legal-analyst

# Use the startup script (recommended)
.\start_backend.ps1

# OR manually:
.\venv\Scripts\activate
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### Starting the Frontend (Streamlit)

```bash
# From project root (in a new terminal)
streamlit run frontend/streamlit_app.py
```

The UI will open automatically in your browser at http://localhost:8501

### Using the System

#### Option 1: Full Report (Recommended)
1. Select "Full Report" mode in the sidebar
2. Upload a PDF file
3. Click "Generate Full Report"
4. Wait for processing (2-5 minutes depending on document size)
5. View results and download JSON report

#### Option 2: Quick Analysis (Step-by-Step)
1. Select "Quick Analysis" mode
2. Upload PDF and extract text
3. Build vector index
4. Run individual analyses:
   - Generate Summary
   - Extract Sections
   - Check Rules

## 📡 API Endpoints

### POST /api/extract
Extract text from PDF file.
- **Input:** PDF file (multipart/form-data)
- **Output:** Extracted text and page count

### POST /api/build_index
Build FAISS vector index from text.
- **Input:** `{"text": "...", "document_name": "..."}`
- **Output:** Index metadata

### POST /api/summaries
Generate document summary.
- **Input:** `{"document_name": "..."}`
- **Output:** High-level summary

### POST /api/sections
Extract structured sections (6 categories).
- **Input:** `{"document_name": "...", "categories": [...]}`
- **Output:** Extracted sections with confidence scores

### POST /api/rule_checks
Validate compliance with legal rules.
- **Input:** `{"document_name": "..."}`
- **Output:** Rule check results

### POST /api/full_report
Execute complete analysis pipeline.
- **Input:** PDF file (multipart/form-data)
- **Output:** Complete analysis report

## 🔍 Legal Categories Analyzed

The system extracts information for 6 legal categories:

1. **Definitions** - Key terms and their meanings
2. **Eligibility** - Criteria and requirements
3. **Payments** - Payment structures and calculations
4. **Penalties** - Enforcement and sanctions
5. **Obligations** - Duties and responsibilities
6. **Record Keeping** - Documentation requirements

## ✅ Legal Rules Validated

The system checks compliance with 6 standard legal document rules:

1. **Key Terms Defined** - Document contains clear definitions
2. **Eligibility Criteria Present** - Specifies who qualifies
3. **Authority Responsibilities Specified** - Defines agency duties
4. **Penalties/Enforcement Exist** - Includes enforcement mechanisms
5. **Payment/Entitlement Structure** - Describes payment details
6. **Reporting/Record-keeping** - Specifies documentation requirements

## 🧠 Self-Correction Agent

The system includes an intelligent self-correction agent that:
- Validates extraction completeness
- Assesses evidence quality
- Calculates confidence scores
- Re-queries vector store if needed
- Iterates up to 2 times per category
- Ensures high-quality results

## 📊 Output Format

The system generates structured JSON reports:

```json
{
  "document_name": "example_document",
  "generated_at": "2025-11-20T23:55:00",
  "summary": {
    "title": "...",
    "purpose": "...",
    "key_topics": [...]
  },
  "sections": {
    "definitions": {...},
    "eligibility": {...},
    ...
  },
  "rule_checks": {
    "results": [...],
    "summary": {
      "total_rules": 6,
      "passed": 5,
      "pass_rate": 83.3
    }
  }
}
```

## 🛠️ Technology Stack

- **Backend Framework:** FastAPI
- **Frontend:** Streamlit
- **PDF Processing:** pdfplumber
- **Text Processing:** LangChain
- **Embeddings:** HuggingFace (sentence-transformers)
- **Vector Store:** FAISS (CPU)
- **LLM:** Llama 3.1 70B (via Groq API)
- **Validation:** Pydantic

## 🔒 Security Notes

- API key is stored in `.env` file (not committed to git)
- `.gitignore` prevents sensitive files from being tracked
- CORS is configured for development (update for production)
- File uploads are stored temporarily and can be cleaned up

## 🐛 Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError`
- **Solution:** Ensure virtual environment is activated and dependencies are installed

**Issue:** `GROQ_API_KEY not found`
- **Solution:** Check that `.env` file exists and contains the API key

**Issue:** `Vector store not found`
- **Solution:** Build the index first before running analysis

**Issue:** API timeout on large documents
- **Solution:** Increase timeout in Streamlit app or use smaller documents

### Logging

The system logs to console. To increase verbosity, modify `setup_logging("DEBUG")` in `backend/app/main.py`.

## 📈 Performance

- **PDF Extraction:** ~1-2 seconds per page
- **Index Building:** ~10-30 seconds for typical documents
- **RAG Extraction:** ~5-10 seconds per category
- **Full Report:** ~2-5 minutes for complete analysis

## 🚀 Deployment

### Production Considerations

1. **Environment Variables:** Use proper secrets management
2. **CORS:** Configure specific allowed origins
3. **Rate Limiting:** Add rate limiting middleware
4. **File Storage:** Use cloud storage for uploads
5. **Vector Store:** Consider persistent storage solution
6. **Monitoring:** Add logging and monitoring
7. **Scaling:** Use async workers for concurrent requests

### Docker Deployment (Optional)

Create a `Dockerfile` and `docker-compose.yml` for containerized deployment.

## 📝 License

This project is provided as-is for educational and demonstration purposes.

## 👥 Contributing

This is a demonstration project. For production use, consider:
- Adding comprehensive tests
- Implementing authentication
- Adding database for persistent storage
- Improving error handling
- Adding monitoring and analytics

## 📧 Support

For issues or questions, please refer to the code documentation and comments.

---

**Built with ⚖️ for legal document analysis**
