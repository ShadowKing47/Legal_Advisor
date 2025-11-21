"""
FAISS vector store module for semantic search.
Manages embedding generation, index creation, and retrieval.
"""

import os
import pickle
from pathlib import Path
from typing import List, Dict, Any, Tuple
try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import logging

logger = logging.getLogger(__name__)


class VectorStoreManager:
    """Manages FAISS vector store for document retrieval."""
    
    def __init__(self, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the vector store manager.
        
        Args:
            embedding_model: HuggingFace model name for embeddings
        """
        self.embedding_model_name = embedding_model
        logger.info(f"Initializing embeddings with model: {embedding_model}")
        
        # Initialize HuggingFace embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        self.vector_store = None
        self.document_name = None
    
    def build_index(self, documents: List[Document], document_name: str) -> int:
        """
        Build FAISS index from documents.
        
        Args:
            documents: List of Document objects to index
            document_name: Name of the source document
            
        Returns:
            Number of documents indexed
        """
        if not documents:
            raise ValueError("No documents provided for indexing")
        
        logger.info(f"Building FAISS index for {len(documents)} documents")
        
        # Create FAISS vector store
        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        self.document_name = document_name
        logger.info(f"Successfully built index with {len(documents)} chunks")
        
        return len(documents)
    
    def save_index(self, save_dir: str) -> str:
        """
        Save FAISS index to disk.
        
        Args:
            save_dir: Directory to save the index
            
        Returns:
            Path to saved index
        """
        if self.vector_store is None:
            raise ValueError("No vector store to save. Build index first.")
        
        save_path = Path(save_dir) / f"{self.document_name}_index"
        save_path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        self.vector_store.save_local(str(save_path))
        
        # Save metadata
        metadata = {
            "document_name": self.document_name,
            "embedding_model": self.embedding_model_name,
            "num_documents": len(self.vector_store.docstore._dict)
        }
        
        with open(save_path / "metadata.pkl", "wb") as f:
            pickle.dump(metadata, f)
        
        logger.info(f"Saved index to: {save_path}")
        return str(save_path)
    
    def load_index(self, index_path: str) -> bool:
        """
        Load FAISS index from disk.
        
        Args:
            index_path: Path to the saved index
            
        Returns:
            True if successful
        """
        index_dir = Path(index_path)
        if not index_dir.exists():
            raise FileNotFoundError(f"Index not found: {index_path}")
        
        logger.info(f"Loading index from: {index_path}")
        
        # Load FAISS index
        self.vector_store = FAISS.load_local(
            str(index_dir),
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        
        # Load metadata
        metadata_path = index_dir / "metadata.pkl"
        if metadata_path.exists():
            with open(metadata_path, "rb") as f:
                metadata = pickle.load(f)
                self.document_name = metadata.get("document_name", "unknown")
        
        logger.info(f"Successfully loaded index for: {self.document_name}")
        return True
    
    def search(
        self,
        query: str,
        k: int = 5,
        filter_dict: Dict[str, Any] = None
    ) -> List[Tuple[Document, float]]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            k: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of (Document, score) tuples
        """
        if self.vector_store is None:
            raise ValueError("No vector store loaded. Build or load index first.")
        
        logger.debug(f"Searching for: '{query}' (top {k})")
        
        # Perform similarity search with scores
        results = self.vector_store.similarity_search_with_score(
            query=query,
            k=k,
            filter=filter_dict
        )
        
        logger.debug(f"Found {len(results)} results")
        return results
    
    def search_by_category(
        self,
        category: str,
        k: int = 5
    ) -> List[Document]:
        """
        Search for documents relevant to a specific legal category.
        
        Args:
            category: Legal category (e.g., "definitions", "eligibility")
            k: Number of results to return
            
        Returns:
            List of relevant Documents
        """
        # Category-specific query templates
        category_queries = {
            "definitions": "definitions, terms, meanings, interpretation, glossary",
            "eligibility": "eligibility criteria, qualifications, requirements, entitled, eligible",
            "payments": "payment, amount, calculation, entitlement, benefits, compensation",
            "penalties": "penalty, sanctions, enforcement, violations, offenses, punishment",
            "obligations": "obligations, duties, responsibilities, requirements, must, shall",
            "record_keeping": "records, documentation, reporting, maintain, keep, register"
        }
        
        query = category_queries.get(category.lower(), category)
        results = self.search(query, k=k)
        
        # Return just the documents (without scores)
        return [doc for doc, score in results]
    
    def get_all_documents(self) -> List[Document]:
        """
        Get all documents from the vector store.
        
        Returns:
            List of all Documents
        """
        if self.vector_store is None:
            raise ValueError("No vector store loaded")
        
        # Access the docstore to get all documents
        all_docs = list(self.vector_store.docstore._dict.values())
        return all_docs
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with statistics
        """
        if self.vector_store is None:
            return {"status": "No index loaded"}
        
        all_docs = self.get_all_documents()
        
        return {
            "document_name": self.document_name,
            "total_chunks": len(all_docs),
            "embedding_model": self.embedding_model_name,
            "embedding_dimension": len(self.embeddings.embed_query("test"))
        }


# Convenience functions
def create_vector_store(
    documents: List[Document],
    document_name: str,
    save_dir: str
) -> str:
    """
    Create and save a vector store.
    
    Args:
        documents: Documents to index
        document_name: Name of the document
        save_dir: Directory to save the index
        
    Returns:
        Path to saved index
    """
    manager = VectorStoreManager()
    manager.build_index(documents, document_name)
    return manager.save_index(save_dir)


def load_vector_store(index_path: str) -> VectorStoreManager:
    """
    Load a vector store from disk.
    
    Args:
        index_path: Path to the saved index
        
    Returns:
        VectorStoreManager instance
    """
    manager = VectorStoreManager()
    manager.load_index(index_path)
    return manager
