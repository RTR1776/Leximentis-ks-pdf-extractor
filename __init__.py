"""
Kansas Workers' Compensation Document Processor

A tool for processing Kansas workers' compensation legal documents,
extracting text, creating logical chunks, and preparing data for embedding.
"""

__version__ = "1.0.0"

from kswc_processor.pdf_extraction import extract_text_from_pdf, get_pdf_metadata
from kswc_processor.metadata_extraction import extract_case_info, extract_enhanced_case_info
from kswc_processor.section_processing import identify_sections, clean_section_text
from kswc_processor.chunking import create_logical_chunks, create_chunks_with_metadata
from kswc_processor.processors import process_pdf_file, process_directory, process_single_file

# Public API
__all__ = [
    'extract_text_from_pdf',
    'get_pdf_metadata',
    'extract_case_info',
    'extract_enhanced_case_info',
    'identify_sections',
    'clean_section_text',
    'create_logical_chunks',
    'create_chunks_with_metadata',
    'process_pdf_file',
    'process_directory',
    'process_single_file'
] 