"""
FastAPI endpoint handlers for Mini Legal Analyst System.
Implements all REST API endpoints for document analysis.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
from typing import Dict, Any

from app.schemas import (
    ExtractRequest, ExtractResponse,
    BuildIndexRequest, BuildIndexResponse,
    SummaryRequest, SummaryResponse,
    SectionRequest, SectionResponse,
    RuleCheckRequest, RuleCheckResponse,
    FullReportRequest, FullReportResponse
)
from app.config import get_settings
from core.pdf_extractor import PDFExtractor
from core.preprocessor import TextPreprocessor
from core.vector_store import VectorStoreManager
from core.rag_pipeline import RAGPipeline
from core.self_correction import SelfCorrectionAgent
from core.rule_checker import RuleChecker
from core.json_builder import JSONBuilder
from utils.helpers import sanitize_filename, get_document_name_from_path
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
settings = get_settings()

# Global state for vector stores (in production, use proper state management)
_vector_stores: Dict[str, VectorStoreManager] = {}


@router.post("/extract", response_model=ExtractResponse)
async def extract_pdf_text(file: UploadFile = File(...)):
    """
    Extract text from uploaded PDF file.
    
    Args:
        file: Uploaded PDF file
        
    Returns:
        ExtractResponse with extracted text and metadata
    """
    try:
        logger.info(f"Extracting PDF: {file.filename}")
        
        # Save uploaded file
        file_path = settings.uploads_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text
        extractor = PDFExtractor()
        text, page_count, _ = extractor.extract_text(str(file_path))
        
        return ExtractResponse(
            success=True,
            text=text,
            page_count=page_count,
            message=f"Successfully extracted {len(text)} characters from {page_count} pages"
        )
        
    except Exception as e:
        logger.error(f"Error extracting PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/build_index", response_model=BuildIndexResponse)
async def build_vector_index(request: BuildIndexRequest):
    """
    Build FAISS vector index from extracted text.
    
    Args:
        request: BuildIndexRequest with text and document name
        
    Returns:
        BuildIndexResponse with index metadata
    """
    try:
        logger.info(f"Building index for: {request.document_name}")
        
        # Preprocess text into chunks
        preprocessor = TextPreprocessor(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        documents = preprocessor.process(request.text, request.document_name)
        
        # Build vector store
        vector_store = VectorStoreManager(settings.embedding_model)
        chunk_count = vector_store.build_index(documents, request.document_name)
        
        # Save index
        index_path = vector_store.save_index(str(settings.vector_store_dir))
        
        # Store in global state
        _vector_stores[request.document_name] = vector_store
        
        return BuildIndexResponse(
            success=True,
            chunk_count=chunk_count,
            index_path=index_path,
            message=f"Successfully built index with {chunk_count} chunks"
        )
        
    except Exception as e:
        logger.error(f"Error building index: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/summaries", response_model=SummaryResponse)
async def generate_summary(request: SummaryRequest):
    """
    Generate document summary.
    
    Args:
        request: SummaryRequest with document name
        
    Returns:
        SummaryResponse with summary data
    """
    try:
        logger.info(f"Generating summary for: {request.document_name}")
        
        # Get vector store
        vector_store = _get_vector_store(request.document_name)
        
        # Generate summary
        rag_pipeline = RAGPipeline(vector_store)
        result = rag_pipeline.generate_summary()
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("message"))
        
        return SummaryResponse(
            success=True,
            summary=result["summary"],
            message="Summary generated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sections", response_model=SectionResponse)
async def extract_sections(request: SectionRequest):
    """
    Extract structured sections from document.
    
    Args:
        request: SectionRequest with document name and categories
        
    Returns:
        SectionResponse with extracted sections
    """
    try:
        logger.info(f"Extracting sections for: {request.document_name}")
        
        # Get vector store
        vector_store = _get_vector_store(request.document_name)
        
        # Extract categories
        rag_pipeline = RAGPipeline(vector_store)
        extractions = {}
        
        for category in request.categories:
            extractions[category] = rag_pipeline.extract_category(category)
        
        # Apply self-correction
        logger.info("Applying self-correction to extractions")
        correction_agent = SelfCorrectionAgent(vector_store)
        validated_extractions = correction_agent.validate_all_categories(extractions)
        
        return SectionResponse(
            success=True,
            sections=validated_extractions,
            message=f"Successfully extracted {len(validated_extractions)} categories"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error extracting sections: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rule_checks", response_model=RuleCheckResponse)
async def check_rules(request: RuleCheckRequest):
    """
    Perform legal rule compliance checks.
    
    Args:
        request: RuleCheckRequest with document name
        
    Returns:
        RuleCheckResponse with rule check results
    """
    try:
        logger.info(f"Checking rules for: {request.document_name}")
        
        # Get vector store
        vector_store = _get_vector_store(request.document_name)
        
        # Check rules
        rule_checker = RuleChecker(vector_store)
        rule_results = rule_checker.check_all_rules()
        
        return RuleCheckResponse(
            success=True,
            rule_checks=rule_results,
            message=f"Successfully checked {len(rule_results)} rules"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking rules: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/full_report", response_model=FullReportResponse)
async def generate_full_report(file: UploadFile = File(...)):
    """
    Execute complete analysis pipeline and generate full report.
    
    Args:
        file: Uploaded PDF file
        
    Returns:
        FullReportResponse with complete analysis
    """
    try:
        document_name = sanitize_filename(file.filename)
        logger.info(f"Generating full report for: {document_name}")
        
        # Step 1: Extract PDF
        logger.info("Step 1/5: Extracting PDF text")
        file_path = settings.uploads_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        extractor = PDFExtractor()
        text, page_count, _ = extractor.extract_text(str(file_path))
        
        # Step 2: Build index
        logger.info("Step 2/5: Building vector index")
        preprocessor = TextPreprocessor(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        documents = preprocessor.process(text, document_name)
        
        vector_store = VectorStoreManager(settings.embedding_model)
        chunk_count = vector_store.build_index(documents, document_name)
        index_path = vector_store.save_index(str(settings.vector_store_dir))
        
        # Step 3: Generate summary
        logger.info("Step 3/5: Generating summary")
        rag_pipeline = RAGPipeline(vector_store)
        summary_result = rag_pipeline.generate_summary()
        summary_data = summary_result.get("summary", {})
        
        # Step 4: Extract sections with self-correction
        logger.info("Step 4/5: Extracting sections")
        extractions = rag_pipeline.extract_all_categories()
        
        correction_agent = SelfCorrectionAgent(vector_store)
        sections_data = correction_agent.validate_all_categories(extractions)
        
        # Step 5: Check rules
        logger.info("Step 5/5: Checking compliance rules")
        rule_checker = RuleChecker(vector_store)
        rule_results = rule_checker.check_all_rules()
        
        # Build final report
        logger.info("Building final JSON report")
        json_builder = JSONBuilder(str(settings.reports_dir))
        
        metadata = {
            "file_name": file.filename,
            "page_count": page_count,
            "chunk_count": chunk_count,
            "index_path": index_path
        }
        
        report_path = json_builder.build_final_report(
            document_name=document_name,
            summary_data=summary_data,
            sections_data=sections_data,
            rule_results=rule_results,
            metadata=metadata
        )
        
        return FullReportResponse(
            success=True,
            report_path=report_path,
            summary=summary_data,
            sections=sections_data,
            rule_checks=rule_results,
            metadata=metadata,
            message="Full analysis completed successfully"
        )
        
    except Exception as e:
        logger.error(f"Error generating full report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def _get_vector_store(document_name: str) -> VectorStoreManager:
    """
    Get vector store for a document.
    
    Args:
        document_name: Name of the document
        
    Returns:
        VectorStoreManager instance
        
    Raises:
        HTTPException: If vector store not found
    """
    if document_name in _vector_stores:
        return _vector_stores[document_name]
    
    # Try to load from disk
    index_path = settings.vector_store_dir / f"{document_name}_index"
    if index_path.exists():
        logger.info(f"Loading vector store from disk: {index_path}")
        vector_store = VectorStoreManager(settings.embedding_model)
        vector_store.load_index(str(index_path))
        _vector_stores[document_name] = vector_store
        return vector_store
    
    raise HTTPException(
        status_code=404,
        detail=f"Vector store not found for document: {document_name}. Please build index first."
    )
