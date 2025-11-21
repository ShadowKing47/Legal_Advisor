"""
Text preprocessing and chunking module using LangChain.
Splits documents into semantic chunks with metadata enrichment.
"""

import re
from typing import List, Dict, Any
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.schema import Document
import logging

logger = logging.getLogger(__name__)


class TextPreprocessor:
    """Preprocesses and chunks text for vector storage."""
    
    def __init__(self, chunk_size: int = 400, chunk_overlap: int = 50):
        """
        Initialize the text preprocessor.
        
        Args:
            chunk_size: Target size for each chunk (in tokens)
            chunk_overlap: Overlap between consecutive chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize LangChain text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size * 4,  # Approximate chars per token
            chunk_overlap=chunk_overlap * 4,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        # Patterns for detecting section headers
        self.section_patterns = [
            r'^(?:PART|CHAPTER|SECTION|ARTICLE)\s+[IVX\d]+',  # PART I, CHAPTER 1, etc.
            r'^\d+\.\s+[A-Z][A-Za-z\s]+$',  # 1. Introduction
            r'^[A-Z][A-Z\s]{3,}$',  # ALL CAPS HEADERS
        ]
    
    def process(
        self,
        text: str,
        document_name: str = "document",
        page_texts: Dict[int, str] = None
    ) -> List[Document]:
        """
        Process text into chunks with metadata.
        
        Args:
            text: Full text to process
            document_name: Name of the source document
            page_texts: Optional dict mapping page numbers to their text
            
        Returns:
            List of LangChain Document objects with metadata
        """
        logger.info(f"Processing text: {len(text)} characters")
        
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        logger.info(f"Created {len(chunks)} chunks")
        
        # Create Document objects with metadata
        documents = []
        current_section = "Unknown"
        
        for idx, chunk in enumerate(chunks):
            # Detect section header in chunk
            section = self._detect_section(chunk)
            if section:
                current_section = section
            
            # Determine page number (approximate)
            page_number = self._estimate_page_number(chunk, text, page_texts)
            
            # Create metadata
            metadata = {
                "chunk_id": idx,
                "document_name": document_name,
                "section_header": current_section,
                "page_number": page_number,
                "chunk_size": len(chunk)
            }
            
            # Create Document object
            doc = Document(
                page_content=chunk,
                metadata=metadata
            )
            documents.append(doc)
        
        logger.info(f"Created {len(documents)} Document objects with metadata")
        return documents
    
    def _detect_section(self, text: str) -> str:
        """
        Detect section header in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Section header if found, empty string otherwise
        """
        lines = text.split('\n')[:3]  # Check first 3 lines
        
        for line in lines:
            line = line.strip()
            for pattern in self.section_patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    return line
        
        return ""
    
    def _estimate_page_number(
        self,
        chunk: str,
        full_text: str,
        page_texts: Dict[int, str] = None
    ) -> int:
        """
        Estimate page number for a chunk.
        
        Args:
            chunk: Text chunk
            full_text: Full document text
            page_texts: Optional dict of page texts
            
        Returns:
            Estimated page number
        """
        if page_texts:
            # Find which page contains this chunk
            for page_num, page_text in page_texts.items():
                if chunk[:50] in page_text:  # Check first 50 chars
                    return page_num
        
        # Fallback: estimate based on position in full text
        try:
            chunk_position = full_text.index(chunk[:50])
            estimated_page = int((chunk_position / len(full_text)) * 100) + 1
            return min(estimated_page, 100)  # Cap at 100
        except ValueError:
            return 1
    
    def get_chunk_stats(self, documents: List[Document]) -> Dict[str, Any]:
        """
        Get statistics about the chunks.
        
        Args:
            documents: List of Document objects
            
        Returns:
            Dictionary with chunk statistics
        """
        if not documents:
            return {}
        
        chunk_sizes = [len(doc.page_content) for doc in documents]
        sections = set(doc.metadata.get("section_header", "Unknown") for doc in documents)
        
        return {
            "total_chunks": len(documents),
            "avg_chunk_size": sum(chunk_sizes) / len(chunk_sizes),
            "min_chunk_size": min(chunk_sizes),
            "max_chunk_size": max(chunk_sizes),
            "unique_sections": len(sections),
            "sections": list(sections)
        }


# Convenience function for direct use
def preprocess_text(text: str, document_name: str = "document") -> List[Document]:
    """
    Preprocess text into chunks.
    
    Args:
        text: Text to process
        document_name: Name of the source document
        
    Returns:
        List of Document objects
    """
    preprocessor = TextPreprocessor()
    return preprocessor.process(text, document_name)
