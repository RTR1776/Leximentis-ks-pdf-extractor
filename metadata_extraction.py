"""
Module for extracting workers' compensation case metadata from documents.
"""
import re
from typing import Dict, List, Optional

from kswc_processor.config import CLAIMANT_PATTERNS, DOCKET_PATTERNS, RESPONDENT_PATTERNS

def extract_case_info(text: str) -> Dict[str, str]:
    """
    Extract basic case metadata including claimant name and docket/case number.
    
    Args:
        text: Text from the document, typically first few pages
        
    Returns:
        Dictionary with extracted case information
    """
    case_info = {
        "claimant_name": "Unknown",
        "docket_number": "Unknown",
        "respondent_name": "Unknown"
    }
    
    # Extract claimant name
    for pattern in CLAIMANT_PATTERNS:
        match = re.search(pattern, text)
        if match:
            name = match.group(1).strip()
            # Validate name - should be more than one word and uppercase
            if ' ' in name and name.isupper():
                case_info['claimant_name'] = name
                break
    
    # Extract docket/case number
    for pattern in DOCKET_PATTERNS:
        match = re.search(pattern, text)
        if match:
            case_info['docket_number'] = match.group(1).strip()
            break
    
    # Extract respondent name
    for pattern in RESPONDENT_PATTERNS:
        match = re.search(pattern, text)
        if match:
            name = match.group(1).strip()
            if ' ' in name and name.isupper():
                case_info['respondent_name'] = name
                break
    
    return case_info

def extract_enhanced_case_info(pages: List[str]) -> Dict[str, str]:
    """
    Enhanced extraction of worker comp case information using multiple pages.
    
    Args:
        pages: List of document pages
        
    Returns:
        Dictionary with extracted case information
    """
    # Use first few pages for metadata extraction
    full_text = "\n".join(pages[:3]) if len(pages) >= 3 else "\n".join(pages)
    
    # Use the basic extraction function
    return extract_case_info(full_text) 