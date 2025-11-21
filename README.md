# Mini Legal Analyst System

A production-ready RAG-based legal document analysis system with **premium glassmorphism UI**, self-correction capabilities, and automated workflow. Built using FastAPI, Streamlit, LangChain, and Llama 3.3 via Groq.

## 🎯 Overview

This system provides comprehensive analysis of legal documents through:
- **PDF Extraction** with intelligent text cleaning
- **Automated Vector Indexing** using FAISS and HuggingFace embeddings
- **RAG Pipeline** powered by Llama 3.3 (via Groq)
- **Self-Correction Agent** with reflection loop for quality assurance
- **Rule Validation** against 6 key legal document requirements
- **Structured JSON Reports** with complete analysis results
- **Premium Dark-Theme Glassmorphism UI** with neon accents and animations

## ✨ New Features

### 🎨 Premium UI/UX
- **Cinematic gradient hero banner** with pulsing animation
- **Floating glass navigation sidebar** with blur effects
- **Neon-accented section headers** with glowing borders
- **Animated gradient progress bars** with shimmer effects
- **Glowing PASS/FAIL badges** with pulsing animations
- **VS Code-style JSON viewer** with syntax highlighting
- **Glassmorphism cards** with frosted-glass effects
- **Responsive layouts** with improved spacing

### 🔄 Automated Workflow
- **Auto-build vector index** after PDF extraction (no manual step)
- **Simultaneous analysis results** - all three analyses can be open at once
- **Download JSON buttons** for each analysis type
- **Streamlined 3-step process**: Upload → Extract → Analyze

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │  ← Premium Glassmorphism Interface
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
│  • RAG Pipeline (Groq + Llama 3.3)  │
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
│   │   ├── config.py            # Configuration (Llama 3.3)
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
│   └── streamlit_app.py         # Premium Glassmorphism UI
├── data/
│   ├── uploads/                 # Uploaded PDFs
│   ├── vector_store/            # FAISS indices
│   └── reports/                 # Generated reports
├── .env                         # Environment variables (not in git)
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
├── start_all.ps1                # Start both services
├── start_backend.ps1            # Start backend only
├── start_frontend.ps1           # Start frontend only
├── stop_all.ps1                 # Stop all services
├── restart_services.ps1         # Restart services
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (tested on Python 3.13)
- Groq API key (free tier available at https://console.groq.com)

### One-Command Setup

```powershell
# Start everything at once
.\start_all.ps1
```

This will:
1. Activate virtual environment
2. Start backend (http://localhost:8000)
3. Start frontend (http://localhost:8501)
4. Open UI in your browser

### Manual Setup

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Advanced Configuration

Modify `backend/app/config.py` for:
- LLM model (default: `llama-3.3-70b-versatile`)
- Chunk size and overlap
- Retrieval settings
- Self-correction thresholds

## 🎮 Usage

### Quick Analysis Mode (Recommended)

**New Streamlined Workflow:**

1. **Upload PDF** → Choose your legal document
2. **Extract Text** → Click "Extract Text" button
3. **Auto Index** → Vector index builds automatically
4. **Run Analyses** → Click any/all analysis buttons:
   - 📊 Generate Summary
   - 📑 Extract Sections
   - ✅ Check Rules
5. **View Results** → All results appear in separate glass cards
6. **Download JSON** → Export each analysis as JSON

**Key Features:**
- ✅ No manual index building required
- ✅ All three analyses can be open simultaneously
- ✅ Download JSON for each analysis type
- ✅ Results persist when running other analyses

### Full Report Mode

1. Select "Full Report" in sidebar
2. Upload PDF file
3. Click "Generate Full Report"
4. Wait 2-5 minutes for complete analysis
5. View comprehensive results
6. Download complete JSON report

## 📡 API Endpoints

### POST /api/extract
Extract text from PDF file.
- **Input:** PDF file (multipart/form-data)
- **Output:** `{"text": "...", "page_count": 10}`

### POST /api/build_index
Build FAISS vector index from text.
- **Input:** `{"text": "...", "document_name": "..."}`
- **Output:** `{"chunk_count": 50, "status": "success"}`

### POST /api/summaries
Generate document summary.
- **Input:** `{"document_name": "..."}`
- **Output:** `{"summary": {"title": "...", "purpose": "...", "key_topics": [...]}}`

### POST /api/sections
Extract structured sections (6 categories).
- **Input:** `{"document_name": "...", "categories": [...]}`
- **Output:** `{"sections": {"definitions": {...}, ...}}`

### POST /api/rule_checks
Validate compliance with legal rules.
- **Input:** `{"document_name": "..."}`
- **Output:** `{"rule_checks": [{"rule": "...", "status": "pass", ...}]}`

### POST /api/full_report
Execute complete analysis pipeline.
- **Input:** PDF file (multipart/form-data)
- **Output:** Complete analysis report with all sections

### GET /health
Health check endpoint.
- **Output:** `{"status": "healthy"}`

### GET /docs
Interactive API documentation (Swagger UI).

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
- Calculates confidence scores (0-100%)
- Re-queries vector store if needed
- Iterates up to 2 times per category
- Ensures high-quality results

## 📊 Output Format

The system generates structured JSON reports with syntax highlighting:

```json
{
  "document_name": "example_document",
  "generated_at": "2025-11-21T23:00:00",
  "summary": {
    "title": "Universal Credit Act 2025",
    "document_type": "Legislation",
    "purpose": "Establish universal credit system",
    "key_topics": ["Social Security", "Benefits", "Eligibility"]
  },
  "sections": {
    "definitions": {
      "data": {...},
      "confidence": {"overall": 95.0},
      "sources": ["Page 1, Section 2.1"]
    }
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

- **Backend:** FastAPI
- **Frontend:** Streamlit with custom CSS
- **PDF:** pdfplumber
- **Text:** LangChain
- **Embeddings:** HuggingFace (sentence-transformers)
- **Vector Store:** FAISS (CPU)
- **LLM:** Llama 3.3 70B (Groq API)
- **Validation:** Pydantic v2

## 🎨 UI Features

### Design System
- **Colors:** Blue (#4a6cf7) → Purple (#8f6bff) → Pink (#ff6b9d)
- **Background:** Radial gradient dark theme
- **Cards:** Frosted glass with backdrop blur
- **Animations:** Pulse, shimmer, glow effects

## 🐛 Troubleshooting

### Common Issues

**`GROQ_API_KEY not found` or `401 Invalid API Key`**
1. Check `.env` file exists
2. Verify API key at https://console.groq.com
3. Restart backend: `.\restart_services.ps1`

**`UnicodeDecodeError` when starting backend**
- Run `python update_api_key.py` to fix BOM issue

**Backend won't start**
1. Run `.\stop_all.ps1`
2. Run `.\start_all.ps1`

### Utility Scripts

- `test_key.py` - Validate Groq API key
- `update_api_key.py` - Update `.env` files
- `verify_env.py` - Check `.env` encoding

## 📈 Performance

- **PDF Extraction:** ~1-2 seconds/page
- **Index Building:** ~10-30 seconds (automatic)
- **RAG Extraction:** ~5-10 seconds/category
- **Full Report:** ~2-5 minutes

## 📝 Scripts Reference

| Script | Purpose |
|--------|---------|
| `start_all.ps1` | Start both services |
| `stop_all.ps1` | Stop all processes |
| `restart_services.ps1` | Restart services |

## 📚 Documentation

- [INSTALL.md](INSTALL.md) - Installation guide
- [QUICKSTART.md](QUICKSTART.md) - Quick start
- API Docs: http://localhost:8000/docs

---

**Built with ⚖️ for legal document analysis**

**Version:** 2.0 - Premium Glassmorphism Edition
