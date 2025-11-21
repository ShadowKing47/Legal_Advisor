"""
Pydantic schemas for API request/response models.
Ensures type safety and validation across all endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


# ============================================================================
# PDF Extraction Schemas
# ============================================================================

class ExtractRequest(BaseModel):
    """Request model for PDF text extraction."""
    file_path: str = Field(..., description="Path to the uploaded PDF file")


class ExtractResponse(BaseModel):
    """Response model for PDF text extraction."""
    success: bool
    text: str = Field(..., description="Extracted and cleaned text from PDF")
    page_count: int = Field(..., description="Number of pages in the PDF")
    message: str = ""


# ============================================================================
# Vector Store Schemas
# ============================================================================

class BuildIndexRequest(BaseModel):
    """Request model for building FAISS vector index."""
    text: str = Field(..., description="Text to chunk and index")
    document_name: str = Field(..., description="Name of the source document")


class BuildIndexResponse(BaseModel):
    """Response model for vector index creation."""
    success: bool
    chunk_count: int = Field(..., description="Number of chunks created")
    index_path: str = Field(..., description="Path to saved FAISS index")
    message: str = ""


# ============================================================================
# Summary Schemas
# ============================================================================

class SummaryRequest(BaseModel):
    """Request model for document summarization."""
    document_name: str = Field(..., description="Name of the indexed document")


class SummaryResponse(BaseModel):
    """Response model for document summary."""
    success: bool
    summary: Dict[str, Any] = Field(default_factory=dict, description="Document summary data")
    message: str = ""


# ============================================================================
# Section Extraction Schemas
# ============================================================================

class SectionRequest(BaseModel):
    """Request model for structured section extraction."""
    document_name: str = Field(..., description="Name of the indexed document")
    categories: List[str] = Field(
        default=["definitions", "eligibility", "payments", "penalties", "obligations", "record_keeping"],
        description="Legal categories to extract"
    )


class SectionResponse(BaseModel):
    """Response model for section extraction."""
    success: bool
    sections: Dict[str, Any] = Field(default_factory=dict, description="Extracted sections by category")
    message: str = ""


# ============================================================================
# Rule Check Schemas
# ============================================================================

class RuleResult(BaseModel):
    """Individual rule check result."""
    rule: str = Field(..., description="Rule description")
    status: str = Field(..., description="pass or fail")
    evidence: str = Field(..., description="Supporting evidence or reference")
    confidence: float = Field(..., ge=0, le=100, description="Confidence percentage (0-100)")


class RuleCheckRequest(BaseModel):
    """Request model for legal rule validation."""
    document_name: str = Field(..., description="Name of the indexed document")


class RuleCheckResponse(BaseModel):
    """Response model for rule checks."""
    success: bool
    rule_checks: List[RuleResult] = Field(default_factory=list, description="Results for all rule checks")
    message: str = ""


# ============================================================================
# Full Report Schemas
# ============================================================================

class FullReportRequest(BaseModel):
    """Request model for complete document analysis."""
    file_path: str = Field(..., description="Path to the uploaded PDF file")
    document_name: str = Field(..., description="Name of the document")


class FullReportResponse(BaseModel):
    """Response model for full analysis report."""
    success: bool
    report_path: str = Field(..., description="Path to the generated JSON report")
    summary: Dict[str, Any] = Field(default_factory=dict)
    sections: Dict[str, Any] = Field(default_factory=dict)
    rule_checks: List[RuleResult] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    message: str = ""


# ============================================================================
# Internal Schemas (for processing)
# ============================================================================

class ConfidenceScore(BaseModel):
    """Confidence metrics for self-correction validation."""
    overall: float = Field(..., ge=0, le=100, description="Overall confidence (0-100)")
    completeness: float = Field(..., ge=0, le=100, description="Data completeness score")
    evidence_quality: float = Field(..., ge=0, le=100, description="Evidence quality score")
    needs_correction: bool = Field(..., description="Whether re-processing is needed")


class CategoryExtraction(BaseModel):
    """Extracted data for a single category."""
    category: str
    data: Dict[str, Any]
    confidence: ConfidenceScore
    sources: List[str] = Field(default_factory=list, description="Source chunk references")
