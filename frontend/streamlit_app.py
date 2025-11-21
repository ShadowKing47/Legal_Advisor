"""
Streamlit frontend for Mini Legal Analyst System.
Provides user interface for PDF upload, analysis, and results visualization.
"""

import streamlit as st
import requests
import json
from pathlib import Path
import time

# API Configuration
API_BASE_URL = "http://localhost:8000/api"

# Page configuration
st.set_page_config(
    page_title="Mini Legal Analyst",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Dark-Theme Glassmorphism CSS
st.markdown("""
<style>
    /* Dark Theme Base with Radial Gradients */
    .stApp {
        background: radial-gradient(ellipse at top, #1a1a2e 0%, #0f0f1e 50%, #050510 100%);
        color: #e0e0e0;
    }
    
    /* Glassmorphism Card Containers */
    .glass-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(74, 108, 247, 0.3);
    }
    
    /* Cinematic Gradient Hero Banner */
    .hero-banner {
        background: radial-gradient(circle at 30% 50%, #4a6cf7 0%, #8f6bff 50%, #ff6b9d 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 50px rgba(74, 108, 247, 0.4);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }
    
    .hero-banner h1 {
        color: white;
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 20px rgba(255,255,255,0.5), 0 0 40px rgba(74, 108, 247, 0.5);
        position: relative;
        z-index: 1;
    }
    
    .hero-banner p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.2rem;
        margin-top: 1rem;
        font-weight: 500;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    /* Floating Glass Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(26, 26, 46, 0.6) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    /* Sidebar Glass Cards */
    .sidebar-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Neon Accent Section Headers */
    .neon-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem 0;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid;
        border-image: linear-gradient(90deg, #4a6cf7, #8f6bff, transparent) 1;
        position: relative;
    }
    
    .neon-header::before {
        content: '';
        position: absolute;
        left: 0;
        bottom: -2px;
        width: 100px;
        height: 2px;
        background: linear-gradient(90deg, #4a6cf7, #8f6bff);
        box-shadow: 0 0 10px #4a6cf7, 0 0 20px #8f6bff;
    }
    
    .neon-header h2 {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 10px rgba(74, 108, 247, 0.5);
    }
    
    /* Gradient Neon Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4a6cf7 0%, #8f6bff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(74, 108, 247, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 6px 25px rgba(74, 108, 247, 0.6), 0 0 30px rgba(143, 107, 255, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: scale(0.98) !important;
    }
    
    /* Glowing PASS/FAIL Badges */
    .badge-pass {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        background: linear-gradient(135deg, #10b981, #34d399);
        color: white;
        border: 1px solid rgba(16, 185, 129, 0.5);
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.6), 0 0 30px rgba(16, 185, 129, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .badge-fail {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ef4444, #f87171);
        color: white;
        border: 1px solid rgba(239, 68, 68, 0.5);
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.6), 0 0 30px rgba(239, 68, 68, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
        animation: pulse-red 2s ease-in-out infinite;
    }
    
    @keyframes pulse-red {
        0%, 100% { box-shadow: 0 0 15px rgba(239, 68, 68, 0.6), 0 0 30px rgba(239, 68, 68, 0.3); }
        50% { box-shadow: 0 0 25px rgba(239, 68, 68, 0.8), 0 0 50px rgba(239, 68, 68, 0.5); }
    }
    
    /* Animated Gradient Progress Bar */
    .fancy-progress-container {
        width: 100%;
        height: 28px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 14px;
        overflow: hidden;
        position: relative;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .fancy-progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #4a6cf7 0%, #8f6bff 50%, #ff6b9d 100%);
        background-size: 200% 100%;
        border-radius: 14px;
        transition: width 0.5s ease;
        position: relative;
        overflow: hidden;
        animation: gradient-shift 3s ease infinite;
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .fancy-progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .fancy-progress-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 0.8rem;
        font-weight: 700;
        color: white;
        text-shadow: 0 2px 5px rgba(0,0,0,0.5);
        z-index: 10;
    }
    
    /* VS Code Style JSON Viewer */
    .vscode-json-container {
        max-height: 350px;
        overflow-y: auto;
        background: #1e1e1e;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(74, 108, 247, 0.3);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5), 0 0 15px rgba(74, 108, 247, 0.2);
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    }
    
    .vscode-json-container pre {
        margin: 0;
        color: #d4d4d4;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    .vscode-json-container::-webkit-scrollbar {
        width: 10px;
    }
    
    .vscode-json-container::-webkit-scrollbar-track {
        background: #252526;
        border-radius: 5px;
    }
    
    .vscode-json-container::-webkit-scrollbar-thumb {
        background: #4a6cf7;
        border-radius: 5px;
    }
    
    .vscode-json-container::-webkit-scrollbar-thumb:hover {
        background: #8f6bff;
    }
    
    /* Neon Divider */
    .neon-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #4a6cf7, #8f6bff, transparent);
        margin: 2.5rem 0;
        border: none;
        box-shadow: 0 0 10px rgba(74, 108, 247, 0.5);
    }
    
    /* Enhanced Metrics */
    div[data-testid="stMetricValue"] {
        color: #4a6cf7 !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(74, 108, 247, 0.3);
    }
    
    /* File Uploader Styling */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1rem;
        border: 2px dashed rgba(74, 108, 247, 0.3);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border-left: 4px solid #10b981 !important;
        border-radius: 8px !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 8px !important;
    }
    
    .stInfo {
        background: rgba(74, 108, 247, 0.1) !important;
        border-left: 4px solid #4a6cf7 !important;
        border-radius: 8px !important;
    }
    
    /* Hide empty glass cards and sidebar cards */
    .glass-card:empty,
    .sidebar-card:empty {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
        height: 0 !important;
    }
    
    /* Prevent empty divs from taking up space */
    div:empty {
        margin: 0;
        padding: 0;
        height: 0;
    }
    
    /* Legacy compatibility classes */
    .card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 1.5rem;
    }
    
    .card:empty {
        display: none !important;
    }
    
    .status-pass { color: #10b981; font-weight: bold; }
    .status-fail { color: #ef4444; font-weight: bold; }
    .confidence-high { color: #10b981; }
    .confidence-medium { color: #fbbf24; }
    .confidence-low { color: #ef4444; }
</style>
""", unsafe_allow_html=True)


def fancy_progress(percent: int, label: str = ""):
    """Display a custom animated gradient progress bar."""
    html = f"""
    <div class="fancy-progress-container">
        <div class="fancy-progress-bar" style="width: {percent}%;">
            <div class="fancy-progress-text">{percent}% {label}</div>
        </div>
    </div>
    """
    return st.markdown(html, unsafe_allow_html=True)


def scroll_json(obj: dict, max_height: int = 350):
    """Display JSON in a VS Code-style scrollable container with syntax highlighting."""
    json_str = json.dumps(obj, indent=2)
    
    # Apply syntax highlighting
    import re
    
    # Highlight strings (values)
    json_str = re.sub(r'": "([^"]*)"', r'": <span style="color: #ce9178;">"\1"</span>', json_str)
    
    # Highlight keys
    json_str = re.sub(r'"([^"]+)":', r'<span style="color: #9cdcfe;">"\1"</span>:', json_str)
    
    # Highlight numbers
    json_str = re.sub(r': (-?\d+\.?\d*)', r': <span style="color: #b5cea8;">\1</span>', json_str)
    
    # Highlight booleans
    json_str = re.sub(r': (true|false)', r': <span style="color: #569cd6;">\1</span>', json_str)
    
    # Highlight null
    json_str = re.sub(r': (null)', r': <span style="color: #569cd6;">\1</span>', json_str)
    
    # Highlight brackets and braces
    json_str = re.sub(r'(\{|\}|\[|\])', r'<span style="color: #ffd700;">\1</span>', json_str)
    
    html = f"""
    <div class="vscode-json-container" style="max-height: {max_height}px;">
        <pre>{json_str}</pre>
    </div>
    """
    return st.markdown(html, unsafe_allow_html=True)


def neon_divider():
    """Display a neon-styled divider."""
    return st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)


def neon_header(icon: str, text: str):
    """Display a neon-accented section header."""
    html = f"""
    <div class="neon-header">
        <span style="font-size: 1.5rem;">{icon}</span>
        <h2>{text}</h2>
    </div>
    """
    return st.markdown(html, unsafe_allow_html=True)



def main():
    """Main application function."""
    
    # Cinematic Hero Banner
    st.markdown('''
    <div class="hero-banner">
        <h1>⚖️ Mini Legal Analyst System</h1>
        <p>Production-ready RAG-based legal document analysis with self-correction</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Floating Glass Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown('### 📋 About', unsafe_allow_html=True)
        st.info("""
        This system analyzes legal documents using:
        
        📄 **PDF Extraction** - Text cleaning
        
        🔍 **Vector Search** - FAISS indexing
        
        🤖 **RAG Pipeline** - Llama 3.3
        
        ✨ **Self-Correction** - AI agent
        
        ✅ **Rule Validation** - 6 legal rules
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown('### 🔧 Settings', unsafe_allow_html=True)
        analysis_mode = st.radio(
            "Analysis Mode",
            ["Quick Analysis", "Full Report"],
            help="Quick: Step-by-step | Full: Complete pipeline"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    if analysis_mode == "Full Report":
        full_report_mode()
    else:
        quick_analysis_mode()


def full_report_mode():
    """Full report generation mode."""
    neon_header("📄", "Full Report Generation")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("Upload a PDF to generate a comprehensive analysis report.")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a legal document (e.g., Universal Credit Act 2025)"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🚀 Generate Full Report", type="primary", use_container_width=True):
                generate_full_report(uploaded_file)
        with col2:
            st.info("This will extract text, build index, generate summaries, extract sections, and check compliance rules.")
    
    st.markdown('</div>', unsafe_allow_html=True)


def quick_analysis_mode():
    """Quick step-by-step analysis mode."""
    neon_header("🔍", "Quick Analysis (Step-by-Step)")
    
    # Initialize session state
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = None
    if 'document_name' not in st.session_state:
        st.session_state.document_name = None
    if 'index_built' not in st.session_state:
        st.session_state.index_built = False
    if 'summary_data' not in st.session_state:
        st.session_state.summary_data = None
    if 'sections_data' not in st.session_state:
        st.session_state.sections_data = None
    if 'rules_data' not in st.session_state:
        st.session_state.rules_data = None
    
    # Step 1: Upload and Extract
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('#### 📤 Step 1: Upload PDF', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'], key="quick_upload")
    
    if uploaded_file is not None:
        if st.button("📤 Extract Text", type="primary"):
            # Extract text
            extract_text(uploaded_file)
            
            # Automatically build index after extraction
            if st.session_state.extracted_text:
                st.markdown('---')
                st.markdown('#### 🔨 Building vector index...', unsafe_allow_html=True)
                build_index()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 3: Analysis Options (shown immediately after index is built)
    if st.session_state.index_built:
        neon_divider()
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('#### 🎯 Step 3: Run Analysis', unsafe_allow_html=True)
        st.write(f"**Document:** {st.session_state.document_name}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Generate Summary", use_container_width=True, key="btn_summary"):
                generate_summary_new()
        
        with col2:
            if st.button("📑 Extract Sections", use_container_width=True, key="btn_sections"):
                extract_sections_new()
        
        with col3:
            if st.button("✅ Check Rules", use_container_width=True, key="btn_rules"):
                check_rules_new()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display results in separate glass cards (all can be open simultaneously)
        
        # Summary Results
        if st.session_state.summary_data:
            neon_divider()
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('### 📊 Document Summary', unsafe_allow_html=True)
            
            summary = st.session_state.summary_data
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Title", summary.get("title", "N/A"))
                st.metric("Document Type", summary.get("document_type", "N/A"))
            
            with col2:
                purpose = summary.get("purpose", "N/A")
                st.metric("Purpose", purpose[:50] + "..." if len(purpose) > 50 else purpose)
            
            st.write("**Key Topics:**")
            for topic in summary.get("key_topics", []):
                st.write(f"- {topic}")
            
            with st.expander("View full summary JSON"):
                scroll_json(summary)
            
            # Download button
            st.download_button(
                label="� Download Summary JSON",
                data=json.dumps(summary, indent=2),
                file_name=f"{st.session_state.document_name}_summary.json",
                mime="application/json",
                use_container_width=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Sections Results
        if st.session_state.sections_data:
            neon_divider()
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('### 📑 Extracted Sections', unsafe_allow_html=True)
            
            sections = st.session_state.sections_data
            
            for category, section_data in sections.items():
                with st.expander(f"📂 {category.upper()}", expanded=False):
                    # Show confidence
                    if "confidence" in section_data:
                        conf = section_data["confidence"]
                        confidence_val = conf.get("overall", 0)
                        confidence_class = get_confidence_class(confidence_val)
                        st.markdown(f"**Confidence:** <span class='{confidence_class}'>{confidence_val:.1f}%</span>", unsafe_allow_html=True)
                    
                    # Show data
                    scroll_json(section_data.get("data", {}))
                    
                    # Show sources
                    if section_data.get("sources"):
                        st.write("**Sources:**")
                        for source in section_data["sources"][:3]:
                            st.caption(source)
            
            # Download button
            st.download_button(
                label="� Download Sections JSON",
                data=json.dumps(sections, indent=2),
                file_name=f"{st.session_state.document_name}_sections.json",
                mime="application/json",
                use_container_width=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Rule Checks Results
        if st.session_state.rules_data:
            neon_divider()
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('### ✅ Compliance Rule Checks', unsafe_allow_html=True)
            
            rule_checks = st.session_state.rules_data
            
            # Summary metrics
            passed = sum(1 for r in rule_checks if r["status"] == "pass")
            total = len(rule_checks)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Rules", total)
            with col2:
                st.metric("Passed", passed, delta=None)
            with col3:
                st.metric("Failed", total - passed, delta=None)
            
            # Individual rules
            st.write("**Rule Results:**")
            for rule in rule_checks:
                status_badge = f'<span class="badge-pass">PASS</span>' if rule["status"] == "pass" else f'<span class="badge-fail">FAIL</span>'
                status_icon = "✅" if rule["status"] == "pass" else "❌"
                
                with st.expander(f"{status_icon} {rule['rule']}", expanded=False):
                    st.markdown(f"**Status:** {status_badge}", unsafe_allow_html=True)
                    st.write(f"**Confidence:** {rule['confidence']:.1f}%")
                    st.write(f"**Evidence:** {rule['evidence']}")
            
            # Download button
            st.download_button(
                label="📥 Download Rule Checks JSON",
                data=json.dumps(rule_checks, indent=2),
                file_name=f"{st.session_state.document_name}_rule_checks.json",
                mime="application/json",
                use_container_width=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)


def extract_text(uploaded_file):
    """Extract text from PDF."""
    with st.spinner("Extracting text from PDF..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            response = requests.post(f"{API_BASE_URL}/extract", files=files)
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.extracted_text = data["text"]
                st.session_state.document_name = Path(uploaded_file.name).stem
                
                st.success(f"✅ Extracted {data['page_count']} pages, {len(data['text']):,} characters")
                
                with st.expander("View extracted text (first 1000 chars)"):
                    st.text(data["text"][:1000] + "...")
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def build_index():
    """Build vector index."""
    with st.spinner("Building vector index... This may take a minute."):
        try:
            payload = {
                "text": st.session_state.extracted_text,
                "document_name": st.session_state.document_name
            }
            response = requests.post(f"{API_BASE_URL}/build_index", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.index_built = True
                st.success(f"✅ Built index with {data['chunk_count']} chunks")
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def generate_summary():
    """Generate document summary."""
    with st.spinner("Generating summary..."):
        try:
            payload = {"document_name": st.session_state.document_name}
            response = requests.post(f"{API_BASE_URL}/summaries", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Summary generated")
                
                summary = data["summary"]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Title", summary.get("title", "N/A"))
                    st.metric("Document Type", summary.get("document_type", "N/A"))
                
                with col2:
                    st.metric("Purpose", summary.get("purpose", "N/A")[:50] + "...")
                
                st.write("**Key Topics:**")
                for topic in summary.get("key_topics", []):
                    st.write(f"- {topic}")
                
                with st.expander("View full summary JSON"):
                    scroll_json(summary)
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def extract_sections():
    """Extract structured sections."""
    with st.spinner("Extracting sections with self-correction... This may take a few minutes."):
        try:
            payload = {"document_name": st.session_state.document_name}
            response = requests.post(f"{API_BASE_URL}/sections", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Sections extracted")
                
                sections = data["sections"]
                
                for category, section_data in sections.items():
                    with st.expander(f"📂 {category.upper()}", expanded=False):
                        # Show confidence
                        if "confidence" in section_data:
                            conf = section_data["confidence"]
                            confidence_val = conf.get("overall", 0)
                            confidence_class = get_confidence_class(confidence_val)
                            st.markdown(f"**Confidence:** <span class='{confidence_class}'>{confidence_val:.1f}%</span>", unsafe_allow_html=True)
                        
                        # Show data
                        scroll_json(section_data.get("data", {}))
                        
                        # Show sources
                        if section_data.get("sources"):
                            st.write("**Sources:**")
                            for source in section_data["sources"][:3]:
                                st.caption(source)
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def check_rules():
    """Check compliance rules."""
    with st.spinner("Checking compliance rules..."):
        try:
            payload = {"document_name": st.session_state.document_name}
            response = requests.post(f"{API_BASE_URL}/rule_checks", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Rule checks completed")
                
                rule_checks = data["rule_checks"]
                
                # Summary metrics
                passed = sum(1 for r in rule_checks if r["status"] == "pass")
                total = len(rule_checks)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Rules", total)
                with col2:
                    st.metric("Passed", passed, delta=None)
                with col3:
                    st.metric("Failed", total - passed, delta=None)
                
                # Individual rules
                st.write("**Rule Results:**")
                for rule in rule_checks:
                    status_class = "status-pass" if rule["status"] == "pass" else "status-fail"
                    status_icon = "✅" if rule["status"] == "pass" else "❌"
                    status_badge = f'<span class="badge-pass">PASS</span>' if rule["status"] == "pass" else f'<span class="badge-fail">FAIL</span>'
                    
                    with st.expander(f"{status_icon} {rule['rule']}", expanded=False):
                        st.markdown(f"**Status:** {status_badge}", unsafe_allow_html=True)
                        st.write(f"**Confidence:** {rule['confidence']:.1f}%")
                        st.write(f"**Evidence:** {rule['evidence']}")
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def generate_summary_new():
    """Generate document summary and store in session state."""
    with st.spinner("Generating summary..."):
        try:
            payload = {"document_name": st.session_state.document_name}
            response = requests.post(f"{API_BASE_URL}/summaries", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.summary_data = data["summary"]
                st.success("✅ Summary generated")
                st.rerun()
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def extract_sections_new():
    """Extract structured sections and store in session state."""
    with st.spinner("Extracting sections with self-correction... This may take a few minutes."):
        try:
            payload = {"document_name": st.session_state.document_name}
            response = requests.post(f"{API_BASE_URL}/sections", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.sections_data = data["sections"]
                st.success("✅ Sections extracted")
                st.rerun()
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def check_rules_new():
    """Check compliance rules and store in session state."""
    with st.spinner("Checking compliance rules..."):
        try:
            payload = {"document_name": st.session_state.document_name}
            response = requests.post(f"{API_BASE_URL}/rule_checks", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.rules_data = data["rule_checks"]
                st.success("✅ Rule checks completed")
                st.rerun()
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def generate_full_report(uploaded_file):
    """Generate complete analysis report."""
    progress_container = st.empty()
    status_text = st.empty()
    
    try:
        status_text.text("📤 Uploading and processing PDF...")
        progress_container.markdown(fancy_progress(10, "Starting..."), unsafe_allow_html=True)
        
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        response = requests.post(f"{API_BASE_URL}/full_report", files=files, timeout=300)
        
        progress_container.markdown(fancy_progress(100, "Complete!"), unsafe_allow_html=True)
        time.sleep(0.5)
        
        if response.status_code == 200:
            data = response.json()
            status_text.text("✅ Analysis complete!")
            
            st.success(f"✅ Full report generated: {data['report_path']}")
            
            # Display results
            display_full_report(data)
            
            # Download button
            report_path = Path(data['report_path'])
            if report_path.exists():
                with open(report_path, 'r') as f:
                    report_json = f.read()
                
                st.download_button(
                    label="📥 Download Full Report (JSON)",
                    data=report_json,
                    file_name=f"{Path(uploaded_file.name).stem}_report.json",
                    mime="application/json",
                    type="primary"
                )
        else:
            st.error(f"❌ Error: {response.text}")
            status_text.text("")
            progress_container.empty()
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        status_text.text("")
        progress_container.empty()


def display_full_report(data):
    """Display full report results."""
    neon_divider()
    neon_header("📊", "Analysis Results")
    
    # Summary
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    with st.expander("📄 Document Summary", expanded=True):
        summary = data.get("summary", {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Title:** {summary.get('title', 'N/A')}")
            st.write(f"**Type:** {summary.get('document_type', 'N/A')}")
        with col2:
            st.write(f"**Purpose:** {summary.get('purpose', 'N/A')}")
        
        if summary.get("key_topics"):
            st.write("**Key Topics:**")
            for topic in summary["key_topics"]:
                st.write(f"- {topic}")
        
        with st.expander("View Full JSON"):
            scroll_json(summary)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sections
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    with st.expander("📑 Extracted Sections", expanded=False):
        sections = data.get("sections", {})
        for category, section_data in sections.items():
            st.subheader(category.upper())
            scroll_json(section_data.get("data", {}))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Rule Checks
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    with st.expander("✅ Compliance Rule Checks", expanded=True):
        rule_checks = data.get("rule_checks", [])
        
        passed = sum(1 for r in rule_checks if r["status"] == "pass")
        total = len(rule_checks)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rules", total)
        with col2:
            st.metric("Passed", passed)
        with col3:
            st.metric("Pass Rate", f"{(passed/total*100):.1f}%")
        
        st.write("")
        for rule in rule_checks:
            status_icon = "✅" if rule["status"] == "pass" else "❌"
            status_badge = f'<span class="badge-pass">PASS</span>' if rule["status"] == "pass" else f'<span class="badge-fail">FAIL</span>'
            st.markdown(f"{status_icon} **{rule['rule']}** - {status_badge} ({rule['confidence']:.1f}%)", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def get_confidence_class(confidence: float) -> str:
    """Get CSS class for confidence level."""
    if confidence >= 70:
        return "confidence-high"
    elif confidence >= 40:
        return "confidence-medium"
    else:
        return "confidence-low"


if __name__ == "__main__":
    main()
