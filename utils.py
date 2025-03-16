"""
Utility functions for the workers' compensation processor.
"""
import os
import re
import json
import logging
from typing import List, Dict, Any, Set

from kswc_processor.config import PDF_EXTENSION

def setup_logging(output_file: str) -> logging.Logger:
    """
    Set up logging for the application.
    
    Args:
        output_file: Base output file path to derive log file path
        
    Returns:
        Configured logger
    """
    log_file = f"{output_file}.log"
    
    # Configure logger
    logger = logging.getLogger("kswc_processor")
    logger.setLevel(logging.INFO)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def find_pdf_files(directory: str, pattern: str = None) -> List[str]:
    """
    Find all PDF files in a directory, optionally filtering by pattern.
    
    Args:
        directory: Directory to search
        pattern: Optional regex pattern to filter files
        
    Returns:
        List of PDF file paths
    """
    pdf_files = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(PDF_EXTENSION):
            if pattern is None or re.search(pattern, filename):
                pdf_files.append(os.path.join(directory, filename))
    return pdf_files

def get_processed_files(output_file: str) -> Set[str]:
    """
    Get set of already processed files from an existing output file.
    
    Args:
        output_file: Path to JSONL output file
        
    Returns:
        Set of processed filenames
    """
    processed_files = set()
    
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r') as f:
                for line in f:
                    chunk = json.loads(line)
                    processed_files.add(chunk["metadata"]["filename"])
        except Exception as e:
            # If there's an error, return empty set
            logging.warning(f"Error loading previous results: {e}")
    
    return processed_files

def write_chunks_to_jsonl(chunks: List[Dict[str, Any]], output_file: str, append: bool = False) -> None:
    """
    Write chunks to a JSONL file.
    
    Args:
        chunks: List of chunk dictionaries
        output_file: Path to output file
        append: Whether to append to existing file
    """
    mode = 'a' if append else 'w'
    with open(output_file, mode) as f:
        for chunk in chunks:
            f.write(json.dumps(chunk) + '\n') 