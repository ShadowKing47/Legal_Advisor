"""
Utility helper functions for the Mini Legal Analyst System.
"""

import os
import hashlib
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def get_file_hash(file_path: str) -> str:
    """
    Calculate MD5 hash of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        MD5 hash string
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove extension
    name = Path(filename).stem
    
    # Replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    name = name.strip('. ')
    
    # Limit length
    if len(name) > 100:
        name = name[:100]
    
    return name


def ensure_dir(directory: str) -> Path:
    """
    Ensure directory exists, create if not.
    
    Args:
        directory: Directory path
        
    Returns:
        Path object
    """
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def setup_logging(log_level: str = "INFO") -> None:
    """
    Setup logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def get_document_name_from_path(file_path: str) -> str:
    """
    Extract document name from file path.
    
    Args:
        file_path: Path to file
        
    Returns:
        Sanitized document name
    """
    filename = Path(file_path).stem
    return sanitize_filename(filename)
