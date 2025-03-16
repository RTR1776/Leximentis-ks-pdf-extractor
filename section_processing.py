"""
Module for identifying and processing document sections.
"""
import re
from typing import List, Dict, Tuple, Optional

from kswc_processor.config import SECTION_PATTERNS

def identify_sections(pages: List[str]) -> List[Tuple[str, str, int, int]]:
    """
    Identify document sections and their content.
    
    Args:
        pages: List of document pages
        
    Returns:
        List of tuples, each containing:
        - section_name: Name of the section
        - section_text: Text content of the section
        - page_num: Page number where the section starts
        - start_pos: Position in combined text where section starts
    """
    sections = []
    combined_text = "\n".join(pages)
    
    # Find all section positions
    section_positions = []
    for pattern in SECTION_PATTERNS:
        for match in re.finditer(pattern, combined_text):
            section_name = match.group(0)
            section_positions.append((match.start(), section_name))
    
    # Sort by position
    section_positions.sort(key=lambda x: x[0])
    
    # Extract section content
    for i, (pos, section_name) in enumerate(section_positions):
        start_pos = pos
        if i < len(section_positions) - 1:
            end_pos = section_positions[i+1][0]
        else:
            end_pos = len(combined_text)
        
        # Get the section text
        section_text = combined_text[start_pos:end_pos].strip()
        
        # Get the page number
        page_num = 0
        current_pos = 0
        for i, page in enumerate(pages):
            if start_pos >= current_pos and start_pos < current_pos + len(page):
                page_num = i
                break
            current_pos += len(page) + 1  # +1 for the newline
        
        sections.append((section_name, section_text, page_num, start_pos))
    
    return sections

def clean_section_text(section_text: str) -> str:
    """
    Clean section text to improve quality.
    
    Args:
        section_text: Raw text from a section
        
    Returns:
        Cleaned text
    """
    # Remove the section header from the beginning
    lines = section_text.split('\n')
    if lines and lines[0].isupper():
        section_text = '\n'.join(lines[1:])
    
    # Remove excessive whitespace
    section_text = re.sub(r'\s+', ' ', section_text)
    
    # Fix common OCR errors
    section_text = re.sub(r'(\w)- (\w)', r'\1\2', section_text)  # Remove hyphenation
    
    return section_text.strip() 