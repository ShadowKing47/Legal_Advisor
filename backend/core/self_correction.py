"""
Self-correction agent with reflection loop.
Validates and improves extraction quality through iterative refinement.
"""

from typing import Dict, Any, List
from core.vector_store import VectorStoreManager
from core.rag_pipeline import RAGPipeline
from app.schemas import ConfidenceScore
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)


class SelfCorrectionAgent:
    """Agent that validates and corrects extraction results."""
    
    def __init__(self, vector_store: VectorStoreManager):
        """
        Initialize the self-correction agent.
        
        Args:
            vector_store: VectorStoreManager instance
        """
        self.vector_store = vector_store
        self.rag_pipeline = RAGPipeline(vector_store)
        settings = get_settings()
        self.max_iterations = settings.max_correction_iterations
        self.min_confidence = settings.min_confidence_threshold
    
    def validate_and_correct(
        self,
        category: str,
        initial_extraction: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate extraction and apply corrections if needed.
        
        Args:
            category: Legal category
            initial_extraction: Initial extraction result
            
        Returns:
            Validated and potentially corrected extraction
        """
        logger.info(f"Validating extraction for category: {category}")
        
        current_extraction = initial_extraction
        iteration = 0
        
        while iteration < self.max_iterations:
            # Calculate confidence score
            confidence = self._calculate_confidence(category, current_extraction)
            
            logger.info(
                f"Iteration {iteration + 1}: "
                f"Confidence={confidence.overall:.1f}%, "
                f"Needs correction={confidence.needs_correction}"
            )
            
            # Check if correction is needed
            if not confidence.needs_correction:
                logger.info(f"Extraction validated for {category}")
                return {
                    **current_extraction,
                    "confidence": confidence.dict(),
                    "iterations": iteration + 1,
                    "validated": True
                }
            
            # Apply correction
            logger.info(f"Applying correction for {category}")
            current_extraction = self._apply_correction(category, current_extraction, confidence)
            iteration += 1
        
        # Max iterations reached
        logger.warning(f"Max iterations reached for {category}")
        final_confidence = self._calculate_confidence(category, current_extraction)
        
        return {
            **current_extraction,
            "confidence": final_confidence.dict(),
            "iterations": iteration,
            "validated": False,
            "message": "Max iterations reached without full validation"
        }
    
    def validate_all_categories(
        self,
        extractions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate and correct all category extractions.
        
        Args:
            extractions: Dictionary of category extractions
            
        Returns:
            Validated extractions
        """
        logger.info("Validating all category extractions")
        validated = {}
        
        for category, extraction in extractions.items():
            validated[category] = self.validate_and_correct(category, extraction)
        
        return validated
    
    def _calculate_confidence(
        self,
        category: str,
        extraction: Dict[str, Any]
    ) -> ConfidenceScore:
        """
        Calculate confidence score for an extraction.
        
        Args:
            category: Legal category
            extraction: Extraction result
            
        Returns:
            ConfidenceScore object
        """
        data = extraction.get("data", {})
        sources = extraction.get("sources", [])
        
        # Completeness: Check if data has content
        completeness = self._assess_completeness(category, data)
        
        # Evidence quality: Check if sources are present
        evidence_quality = min(100.0, len(sources) * 20.0) if sources else 0.0
        
        # Overall confidence (weighted average)
        overall = (completeness * 0.7 + evidence_quality * 0.3)
        
        # Determine if correction is needed
        needs_correction = (
            overall < (self.min_confidence * 100) or
            completeness < 50.0 or
            evidence_quality < 30.0
        )
        
        return ConfidenceScore(
            overall=overall,
            completeness=completeness,
            evidence_quality=evidence_quality,
            needs_correction=needs_correction
        )
    
    def _assess_completeness(self, category: str, data: Dict[str, Any]) -> float:
        """
        Assess completeness of extracted data.
        
        Args:
            category: Legal category
            data: Extracted data
            
        Returns:
            Completeness score (0-100)
        """
        if not data:
            return 0.0
        
        # Category-specific completeness checks
        expected_fields = {
            "definitions": ["terms"],
            "eligibility": ["criteria"],
            "payments": ["payment_types"],
            "penalties": ["penalties"],
            "obligations": ["obligations"],
            "record_keeping": ["requirements"]
        }
        
        required = expected_fields.get(category, [])
        if not required:
            # Generic check: any non-empty data
            return 50.0 if data else 0.0
        
        # Check if required fields are present and non-empty
        present_fields = sum(
            1 for field in required
            if field in data and data[field]
        )
        
        if not required:
            return 50.0
        
        field_score = (present_fields / len(required)) * 100
        
        # Check data richness (number of items in lists)
        richness_score = 0.0
        for field in required:
            if field in data and isinstance(data[field], list):
                # More items = higher score (capped at 100)
                richness_score += min(100.0, len(data[field]) * 25.0)
        
        if required:
            richness_score /= len(required)
        
        # Combine field presence and richness
        return (field_score * 0.6 + richness_score * 0.4)
    
    def _apply_correction(
        self,
        category: str,
        extraction: Dict[str, Any],
        confidence: ConfidenceScore
    ) -> Dict[str, Any]:
        """
        Apply correction to improve extraction quality.
        
        Args:
            category: Legal category
            extraction: Current extraction
            confidence: Confidence assessment
            
        Returns:
            Corrected extraction
        """
        logger.info(f"Applying correction: completeness={confidence.completeness:.1f}%")
        
        # If completeness is very low, re-extract with more context
        if confidence.completeness < 30.0:
            logger.info("Low completeness detected, re-extracting with more chunks")
            # Increase retrieval count temporarily
            original_k = self.rag_pipeline.retrieval_k
            self.rag_pipeline.retrieval_k = min(original_k + 3, 10)
            
            corrected = self.rag_pipeline.extract_category(category)
            
            # Restore original setting
            self.rag_pipeline.retrieval_k = original_k
            
            return corrected
        
        # If evidence is weak, try different query
        if confidence.evidence_quality < 50.0:
            logger.info("Weak evidence, attempting alternative retrieval")
            # Re-extract (RAG pipeline will use different retrieval strategy)
            return self.rag_pipeline.extract_category(category)
        
        # Otherwise, return as-is
        return extraction
    
    def get_overall_confidence(
        self,
        validated_extractions: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Get overall confidence metrics across all categories.
        
        Args:
            validated_extractions: Validated category extractions
            
        Returns:
            Dictionary with aggregate confidence metrics
        """
        confidences = []
        
        for category, extraction in validated_extractions.items():
            if "confidence" in extraction:
                conf = extraction["confidence"]
                confidences.append(conf.get("overall", 0.0))
        
        if not confidences:
            return {
                "average_confidence": 0.0,
                "min_confidence": 0.0,
                "max_confidence": 0.0
            }
        
        return {
            "average_confidence": sum(confidences) / len(confidences),
            "min_confidence": min(confidences),
            "max_confidence": max(confidences)
        }
