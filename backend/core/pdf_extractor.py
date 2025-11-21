"""
PDF text extraction module with cleaning and normalization.
Uses pdfplumber for accurate text extraction from legal documents.
"""

import re
import pdfplumber
from pathlib import Path
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class PDFExtractor:
    """Extracts and cleans text from PDF documents."""
    
    def __init__(self):
        """Initialize the PDF extractor."""
        self.header_footer_patterns = [
            r'^\d+\s*$',  # Page numbers
            r'^Page \d+ of \d+$',  # "Page X of Y"
            r'^\d+\s*/\s*\d+$',  # "X / Y"
            r'^©.*$',  # Copyright notices
            r'^Confidential.*$',  # Confidential headers
        ]
    
    def extract_text(self, pdf_path: str) -> Tuple[str, int, Dict[int, str]]:
        """
        Extract text from PDF file with cleaning.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple of (cleaned_text, page_count, page_texts_dict)
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            Exception: If PDF extraction fails
        """
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Extracting text from PDF: {pdf_path}")
        
        page_texts = {}
        all_text = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                page_count = len(pdf.pages)
                logger.info(f"Processing {page_count} pages")
                
                for page_num, page in enumerate(pdf.pages, start=1):
                    # Extract text from page
                    text = page.extract_text()
                    
                    if text:
                        # Clean the text
                        cleaned_text = self._clean_text(text)
                        page_texts[page_num] = cleaned_text
                        all_text.append(cleaned_text)
                        logger.debug(f"Extracted {len(cleaned_text)} chars from page {page_num}")
                
                # Combine all pages
                full_text = "\n\n".join(all_text)
                
                # Final normalization
                full_text = self._normalize_text(full_text)
                
                logger.info(f"Successfully extracted {len(full_text)} characters from {page_count} pages")
                return full_text, page_count, page_texts
                
        except Exception as e:
            logger.error(f"Error extracting PDF: {str(e)}")
            raise Exception(f"Failed to extract PDF: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text by removing headers, footers, and artifacts.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue
            
            # Check if line matches header/footer patterns
            is_header_footer = False
            for pattern in self.header_footer_patterns:
                if re.match(pattern, line.strip(), re.IGNORECASE):
                    is_header_footer = True
                    break
            
            if not is_header_footer:
                cleaned_lines.append(line.strip())
        
        return '\n'.join(cleaned_lines)
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize text by fixing whitespace and formatting issues.
        
        Args:
            text: Text to normalize
            
        Returns:
            Normalized text
        """
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Replace multiple newlines with double newline (paragraph breaks)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Fix hyphenated words split across lines
        text = re.sub(r'-\n', '', text)
        
        # Remove spaces before punctuation
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        
        return text.strip()
    
    def extract_with_metadata(self, pdf_path: str) -> Dict:
        """
        Extract text with additional metadata.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with text, page_count, and page-level data
        """
        full_text, page_count, page_texts = self.extract_text(pdf_path)
        
        return {
            "text": full_text,
            "page_count": page_count,
            "page_texts": page_texts,
            "file_path": str(pdf_path),
            "file_name": Path(pdf_path).name
        }


# Convenience function for direct use
def extract_pdf(pdf_path: str) -> Tuple[str, int]:
    """
    Extract text from PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Tuple of (cleaned_text, page_count)
    """
    extractor = PDFExtractor()
    text, page_count, _ = extractor.extract_text(pdf_path)
    return text, page_count
