"""
Module for extracting text from PDF documents.
"""
import os
import PyPDF2
from typing import List, Dict, Any

def extract_text_from_pdf(pdf_path: str) -> List[str]:
    """
    Extract text from PDF, returning a list of pages.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of strings, each containing the text of one page
    """
    pages = []
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                pages.append(page.extract_text())
        return pages
    except Exception as e:
        raise IOError(f"Error extracting text from PDF {pdf_path}: {str(e)}")

def get_pdf_metadata(pdf_path: str) -> Dict[str, Any]:
    """
    Extract basic metadata from PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary containing metadata like author, title, etc.
    """
    metadata = {
        "filename": os.path.basename(pdf_path),
        "filesize": os.path.getsize(pdf_path)
    }
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            # Add document info if available
            if reader.metadata:
                for key, value in reader.metadata.items():
                    if key.startswith('/'):
                        clean_key = key[1:].lower()  # Remove leading slash and lowercase
                        metadata[clean_key] = value
            metadata["page_count"] = len(reader.pages)
    except Exception as e:
        # Just return basic metadata if we can't extract document info
        metadata["error"] = str(e)
        
    return metadata 