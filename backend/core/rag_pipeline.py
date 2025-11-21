"""
RAG (Retrieval-Augmented Generation) pipeline module.
Combines vector search with LLM generation for structured extraction.
"""

import json
from typing import List, Dict, Any
from langchain_groq import ChatGroq
try:
    from langchain_core.documents import Document
    from langchain_core.messages import HumanMessage, SystemMessage
except ImportError:
    from langchain.schema import Document, HumanMessage, SystemMessage
from core.vector_store import VectorStoreManager
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)


class RAGPipeline:
    """RAG pipeline for legal document analysis."""
    
    # Legal categories to extract
    CATEGORIES = [
        "definitions",
        "eligibility",
        "payments",
        "penalties",
        "obligations",
        "record_keeping"
    ]
    
    def __init__(self, vector_store: VectorStoreManager):
        """
        Initialize the RAG pipeline.
        
        Args:
            vector_store: VectorStoreManager instance with loaded index
        """
        self.vector_store = vector_store
        settings = get_settings()
        
        # Initialize Groq LLM
        logger.info(f"Initializing LLM: {settings.llm_model}")
        self.llm = ChatGroq(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
            groq_api_key=settings.groq_api_key
        )
        
        self.retrieval_k = settings.retrieval_top_k
    
    def extract_category(self, category: str) -> Dict[str, Any]:
        """
        Extract structured information for a specific category.
        
        Args:
            category: Legal category to extract
            
        Returns:
            Dictionary with extracted data and metadata
        """
        if category not in self.CATEGORIES:
            raise ValueError(f"Invalid category: {category}. Must be one of {self.CATEGORIES}")
        
        logger.info(f"Extracting category: {category}")
        
        # Retrieve relevant chunks
        relevant_docs = self.vector_store.search_by_category(category, k=self.retrieval_k)
        
        if not relevant_docs:
            logger.warning(f"No relevant documents found for category: {category}")
            return {
                "category": category,
                "data": {},
                "sources": [],
                "message": "No relevant information found"
            }
        
        # Prepare context from retrieved documents
        context = self._prepare_context(relevant_docs)
        
        # Generate extraction prompt
        prompt = self._create_extraction_prompt(category, context)
        
        # Call LLM
        try:
            response = self._call_llm(prompt)
            extracted_data = self._parse_llm_response(response)
            
            # Add metadata
            sources = [
                f"Page {doc.metadata.get('page_number', 'N/A')}, Chunk {doc.metadata.get('chunk_id', 'N/A')}"
                for doc in relevant_docs
            ]
            
            return {
                "category": category,
                "data": extracted_data,
                "sources": sources,
                "message": "Successfully extracted"
            }
            
        except Exception as e:
            logger.error(f"Error extracting category {category}: {str(e)}")
            return {
                "category": category,
                "data": {},
                "sources": [],
                "message": f"Extraction failed: {str(e)}"
            }
    
    def extract_all_categories(self) -> Dict[str, Any]:
        """
        Extract information for all legal categories.
        
        Returns:
            Dictionary with all category extractions
        """
        logger.info("Extracting all categories")
        results = {}
        
        for category in self.CATEGORIES:
            results[category] = self.extract_category(category)
        
        return results
    
    def generate_summary(self) -> Dict[str, Any]:
        """
        Generate a high-level summary of the document.
        
        Returns:
            Dictionary with summary information
        """
        logger.info("Generating document summary")
        
        # Get a diverse set of chunks
        all_docs = self.vector_store.get_all_documents()
        
        # Sample chunks from different sections
        sample_docs = self._sample_documents(all_docs, n=10)
        context = self._prepare_context(sample_docs)
        
        # Create summary prompt
        prompt = f"""You are a legal document analyst. Based on the following excerpts from a legal document, provide a comprehensive summary.

Document Excerpts:
{context}

Provide a JSON response with the following structure:
{{
    "title": "Document title or main subject",
    "purpose": "Main purpose of the document",
    "scope": "Scope and applicability",
    "key_topics": ["topic1", "topic2", ...],
    "document_type": "Type of legal document (e.g., Act, Regulation, Policy)"
}}

Respond ONLY with valid JSON, no additional text."""
        
        try:
            response = self._call_llm(prompt)
            summary_data = self._parse_llm_response(response)
            
            return {
                "success": True,
                "summary": summary_data,
                "message": "Summary generated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return {
                "success": False,
                "summary": {},
                "message": f"Summary generation failed: {str(e)}"
            }
    
    def _prepare_context(self, documents: List[Document]) -> str:
        """
        Prepare context string from documents.
        
        Args:
            documents: List of Document objects
            
        Returns:
            Formatted context string
        """
        context_parts = []
        for idx, doc in enumerate(documents, 1):
            page = doc.metadata.get('page_number', 'N/A')
            section = doc.metadata.get('section_header', 'N/A')
            content = doc.page_content.strip()
            
            context_parts.append(
                f"[Excerpt {idx}] (Page {page}, Section: {section})\n{content}\n"
            )
        
        return "\n".join(context_parts)
    
    def _create_extraction_prompt(self, category: str, context: str) -> str:
        """
        Create extraction prompt for a specific category.
        
        Args:
            category: Legal category
            context: Retrieved context
            
        Returns:
            Formatted prompt string
        """
        # Category-specific instructions
        category_instructions = {
            "definitions": """Extract all defined terms and their definitions. Format as:
{
    "terms": [
        {"term": "term name", "definition": "definition text", "reference": "section/page"},
        ...
    ]
}""",
            "eligibility": """Extract eligibility criteria and requirements. Format as:
{
    "criteria": [
        {"requirement": "requirement description", "details": "additional details", "reference": "section/page"},
        ...
    ],
    "exclusions": ["exclusion1", "exclusion2", ...]
}""",
            "payments": """Extract payment and entitlement information. Format as:
{
    "payment_types": [
        {"type": "payment type", "amount": "amount or formula", "frequency": "frequency", "reference": "section/page"},
        ...
    ],
    "calculation_method": "description of how payments are calculated"
}""",
            "penalties": """Extract penalties and enforcement mechanisms. Format as:
{
    "penalties": [
        {"violation": "violation description", "penalty": "penalty description", "severity": "severity level", "reference": "section/page"},
        ...
    ],
    "enforcement_authority": "authority responsible for enforcement"
}""",
            "obligations": """Extract obligations and responsibilities. Format as:
{
    "obligations": [
        {"party": "obligated party", "obligation": "obligation description", "deadline": "deadline if any", "reference": "section/page"},
        ...
    ]
}""",
            "record_keeping": """Extract record-keeping and reporting requirements. Format as:
{
    "requirements": [
        {"type": "record type", "retention_period": "how long to keep", "responsible_party": "who maintains", "reference": "section/page"},
        ...
    ],
    "reporting_obligations": ["reporting requirement1", "reporting requirement2", ...]
}"""
        }
        
        instruction = category_instructions.get(category, "Extract relevant information in JSON format.")
        
        prompt = f"""You are a legal document analyst specializing in extracting structured information from legal texts.

Category: {category.upper()}

Context from Document:
{context}

Task: {instruction}

IMPORTANT: Respond ONLY with valid JSON. Do not include any explanatory text, markdown formatting, or code blocks. Just the raw JSON object."""
        
        return prompt
    
    def _call_llm(self, prompt: str) -> str:
        """
        Call the LLM with a prompt.
        
        Args:
            prompt: Prompt string
            
        Returns:
            LLM response text
        """
        messages = [
            SystemMessage(content="You are a precise legal document analyst. Always respond with valid JSON only."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """
        Parse LLM response as JSON.
        
        Args:
            response: LLM response string
            
        Returns:
            Parsed JSON dictionary
        """
        # Clean response (remove markdown code blocks if present)
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            logger.error(f"Response was: {response}")
            # Return empty structure
            return {}
    
    def _sample_documents(self, documents: List[Document], n: int = 10) -> List[Document]:
        """
        Sample documents evenly from the collection.
        
        Args:
            documents: List of all documents
            n: Number of documents to sample
            
        Returns:
            Sampled documents
        """
        if len(documents) <= n:
            return documents
        
        # Sample evenly across the document
        step = len(documents) // n
        return [documents[i * step] for i in range(n)]
