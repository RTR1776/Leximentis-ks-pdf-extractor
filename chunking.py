"""
Module for creating logical text chunks from document sections.
"""
import re
from typing import List, Dict, Any

from kswc_processor.config import MAX_CHUNK_SIZE

def create_logical_chunks(text: str, max_tokens: int = MAX_CHUNK_SIZE) -> List[str]:
    """
    Split text into logical chunks based on paragraphs and size.
    
    Args:
        text: Text to split into chunks
        max_tokens: Maximum tokens (approximate words) per chunk
        
    Returns:
        List of text chunks
    """
    chunks = []
    paragraphs = re.split(r'\n\s*\n', text)
    
    current_chunk = []
    current_size = 0
    
    for para in paragraphs:
        para_size = len(para.split())
        
        if current_size + para_size > max_tokens and current_chunk:
            # Complete current chunk
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_size = para_size
        else:
            current_chunk.append(para)
            current_size += para_size
    
    # Add the final chunk if it exists
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks

def create_chunks_with_metadata(
    section_name: str, 
    section_text: str, 
    metadata: Dict[str, str], 
    max_tokens: int = MAX_CHUNK_SIZE
) -> List[Dict[str, Any]]:
    """
    Create chunks from a section, adding appropriate metadata.
    
    Args:
        section_name: Name of the section
        section_text: Text content of the section
        metadata: Document metadata to include with each chunk
        max_tokens: Maximum tokens per chunk
        
    Returns:
        List of dictionaries, each containing chunk text and metadata
    """
    chunk_dicts = []
    chunks = create_logical_chunks(section_text, max_tokens)
    
    for i, chunk_text in enumerate(chunks):
        # Format text with case info for context
        formatted_text = (
            f"Case: {metadata['docket_number']} | "
            f"Claimant: {metadata['claimant_name']}\n"
            f"Section: {section_name}\n\n{chunk_text}"
        )
        
        # Create chunk dictionary with metadata
        chunk_data = {
            "text": formatted_text,
            "metadata": {
                "docket_number": metadata['docket_number'],
                "claimant_name": metadata['claimant_name'],
                "section": section_name,
                "chunk_index": i,
                "chunk_count": len(chunks),
                "filename": metadata.get('filename', 'unknown')
            }
        }
        
        # Add respondent if available
        if 'respondent_name' in metadata and metadata['respondent_name'] != "Unknown":
            chunk_data["metadata"]["respondent_name"] = metadata['respondent_name']
            
        chunk_dicts.append(chunk_data)
    
    return chunk_dicts 