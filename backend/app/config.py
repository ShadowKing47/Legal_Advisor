"""
Configuration management for Mini Legal Analyst System.
Loads environment variables and provides centralized access to settings.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys - support both lowercase and uppercase env var names
    groq_api_key: str = Field(..., validation_alias="GROQ_API_KEY")
    
    # Paths
    base_dir: Path = Path(__file__).parent.parent.parent
    data_dir: Path = base_dir / "data"
    uploads_dir: Path = data_dir / "uploads"
    vector_store_dir: Path = data_dir / "vector_store"
    reports_dir: Path = data_dir / "reports"
    
    # LLM Settings
    llm_model: str = "llama-3.3-70b-versatile"
    llm_temperature: float = 0.1
    llm_max_tokens: int = 2048
    
    # Embedding Settings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Chunking Settings
    chunk_size: int = 400
    chunk_overlap: int = 50
    
    # RAG Settings
    retrieval_top_k: int = 5
    
    # Self-correction Settings
    max_correction_iterations: int = 2
    min_confidence_threshold: float = 0.7
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True
    )


# Singleton instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create the settings singleton instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
        # Ensure data directories exist
        _settings.uploads_dir.mkdir(parents=True, exist_ok=True)
        _settings.vector_store_dir.mkdir(parents=True, exist_ok=True)
        _settings.reports_dir.mkdir(parents=True, exist_ok=True)
    return _settings
