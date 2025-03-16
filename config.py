"""
Configuration settings for the Kansas Workers' Compensation processor.
Contains regex patterns and other configuration parameters.
"""
from typing import Dict, List, Tuple

# PDF Processing Configuration
MAX_CHUNK_SIZE = 800  # Maximum tokens per chunk
DEFAULT_WORKERS = 4   # Default number of parallel workers

# Document Section Patterns
SECTION_PATTERNS = [
    r'\bAPPEARANCES\b',
    r'\bRECORD AND STIPULATIONS\b', 
    r'\bISSUES\b',
    r'\bFINDINGS OF FACT\b',
    r'\bPRINCIPLES OF LAW( AND ANALYSIS)?\b',
    r'\bANALYSIS\b',
    r'\bCONCLUSION(S)?\b',
    r'\bAWARD\b',
    r'\bORDER\b',
    r'\bDECISION\b'
]

# Metadata Extraction Patterns
CLAIMANT_PATTERNS = [
    # General patterns
    r'([A-Z][A-Z\s\.]+)\s+\)\s*\n\s*Claimant',
    r'([A-Z][A-Z\s\.]+)\s+\d+\s+DOCKET\s+NO\.',
    # Format: NAME vs. RESPONDENT
    r'([A-Z][A-Z\s\.]+)\s+vs\.\s+',
    r'([A-Z][A-Z\s\.]+)\s+VS\.\s+',
    # Special case for common formats where claimant name is in specific position
    r'BEFORE\s+THE\s+[A-Z\s]+\s+APPEALS\s+BOARD\s+([A-Z][A-Z\s\.]+)',
]

DOCKET_PATTERNS = [
    # General docket formats
    r'Docket\s+No\.\s+([\d,\.\-]+)',
    r'DOCKET\s+NO\.\s+([\d,\.\-]+)',
    r'(AP-\d+-\d+-\d+)',
    r'(CS-\d+-\d+-\d+)',
    # Look for standalone docket number format
    r'(?:^|\s)([\d]{3},[\d]{3})(?:$|\s)',
]

RESPONDENT_PATTERNS = [
    # General patterns
    r'VS\.\s*\)\s*\n\s*\)\s*\n\s*([A-Z][A-Z\s\.]+)',
    r'VS\.\s*\)\s*\n\s*([A-Z][A-Z\s\.]+)',
    r'vs\.\s+([A-Z][A-Z\s\.]+)',
    r'RESPONDENT:\s+([A-Z][A-Z\s\.]+)',
]

# File extension patterns
PDF_EXTENSION = ".pdf" 