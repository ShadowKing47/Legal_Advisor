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

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .status-pass {
        color: #28a745;
        font-weight: bold;
    }
    .status-fail {
        color: #dc3545;
        font-weight: bold;
    }
    .confidence-high {
        color: #28a745;
    }
    .confidence-medium {
        color: #ffc107;
    }
    .confidence-low {
        color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function."""
    
    # Header
    st.markdown('<div class="main-header">⚖️ Mini Legal Analyst System</div>', unsafe_allow_html=True)
    st.markdown("**Production-ready RAG-based legal document analysis with self-correction**")
    st.divider()
    
    # Sidebar
    with st.sidebar:
        st.header("📋 About")
        st.info("""
        This system analyzes legal documents using:
        - **PDF Extraction** with text cleaning
        - **Vector Search** with FAISS
        - **RAG Pipeline** with Llama 3.1
        - **Self-Correction** agent
        - **Rule Validation** (6 legal rules)
        """)
        
        st.header("🔧 Settings")
        analysis_mode = st.radio(
            "Analysis Mode",
            ["Quick Analysis", "Full Report"],
            help="Quick: Step-by-step | Full: Complete pipeline"
        )
    
    # Main content
    if analysis_mode == "Full Report":
        full_report_mode()
    else:
        quick_analysis_mode()


def full_report_mode():
    """Full report generation mode."""
    st.markdown('<div class="section-header">📄 Full Report Generation</div>', unsafe_allow_html=True)
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


def quick_analysis_mode():
    """Quick step-by-step analysis mode."""
    st.markdown('<div class="section-header">🔍 Quick Analysis (Step-by-Step)</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = None
    if 'document_name' not in st.session_state:
        st.session_state.document_name = None
    if 'index_built' not in st.session_state:
        st.session_state.index_built = False
    
    # Step 1: Upload and Extract
    st.subheader("Step 1: Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'], key="quick_upload")
    
    if uploaded_file is not None:
        if st.button("📤 Extract Text", type="primary"):
            extract_text(uploaded_file)
    
    # Step 2: Build Index
    if st.session_state.extracted_text:
        st.divider()
        st.subheader("Step 2: Build Vector Index")
        st.write(f"Document: **{st.session_state.document_name}**")
        st.write(f"Text length: **{len(st.session_state.extracted_text):,}** characters")
        
        if st.button("🔨 Build Index", type="primary"):
            build_index()
    
    # Step 3: Analysis Options
    if st.session_state.index_built:
        st.divider()
        st.subheader("Step 3: Run Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Generate Summary", use_container_width=True):
                generate_summary()
        
        with col2:
            if st.button("📑 Extract Sections", use_container_width=True):
                extract_sections()
        
        with col3:
            if st.button("✅ Check Rules", use_container_width=True):
                check_rules()


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
                    st.json(summary)
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
                        st.json(section_data.get("data", {}))
                        
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
                    
                    with st.expander(f"{status_icon} {rule['rule']}", expanded=False):
                        st.markdown(f"**Status:** <span class='{status_class}'>{rule['status'].upper()}</span>", unsafe_allow_html=True)
                        st.write(f"**Confidence:** {rule['confidence']:.1f}%")
                        st.write(f"**Evidence:** {rule['evidence']}")
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def generate_full_report(uploaded_file):
    """Generate complete analysis report."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("📤 Uploading and processing PDF...")
        progress_bar.progress(10)
        
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        response = requests.post(f"{API_BASE_URL}/full_report", files=files, timeout=300)
        
        progress_bar.progress(100)
        
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
            progress_bar.empty()
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        status_text.text("")
        progress_bar.empty()


def display_full_report(data):
    """Display full report results."""
    st.divider()
    st.markdown('<div class="section-header">📊 Analysis Results</div>', unsafe_allow_html=True)
    
    # Summary
    with st.expander("📄 Document Summary", expanded=True):
        summary = data.get("summary", {})
        st.write(f"**Title:** {summary.get('title', 'N/A')}")
        st.write(f"**Type:** {summary.get('document_type', 'N/A')}")
        st.write(f"**Purpose:** {summary.get('purpose', 'N/A')}")
        
        if summary.get("key_topics"):
            st.write("**Key Topics:**")
            for topic in summary["key_topics"]:
                st.write(f"- {topic}")
    
    # Sections
    with st.expander("📑 Extracted Sections", expanded=False):
        sections = data.get("sections", {})
        for category, section_data in sections.items():
            st.subheader(category.upper())
            st.json(section_data.get("data", {}))
    
    # Rule Checks
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
        
        for rule in rule_checks:
            status_icon = "✅" if rule["status"] == "pass" else "❌"
            st.write(f"{status_icon} **{rule['rule']}** - {rule['status'].upper()} ({rule['confidence']:.1f}%)")


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
