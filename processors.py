"""
Main processing functions for workers' compensation documents.
"""
import os
import time
import traceback
import logging
from concurrent.futures import ProcessPoolExecutor
from typing import Dict, List, Any, Tuple, Optional

import tqdm

from kswc_processor.pdf_extraction import extract_text_from_pdf
from kswc_processor.metadata_extraction import extract_enhanced_case_info
from kswc_processor.section_processing import identify_sections, clean_section_text
from kswc_processor.chunking import create_chunks_with_metadata
from kswc_processor.utils import find_pdf_files, get_processed_files, write_chunks_to_jsonl
from kswc_processor.config import MAX_CHUNK_SIZE

def process_pdf_file(pdf_path: str) -> Dict[str, Any]:
    """
    Process a single PDF file and return its chunks.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary with processing results or error details
    """
    try:
        filename = os.path.basename(pdf_path)
        pages = extract_text_from_pdf(pdf_path)
        
        # Get metadata
        metadata = extract_enhanced_case_info(pages)
        metadata['filename'] = filename
        
        # Process document sections
        sections = identify_sections(pages)
        
        file_chunks = []
        for section_name, section_text, page_num, _ in sections:
            # Skip section headers that are too short or just contain the header
            if len(section_text.strip()) <= len(section_name) + 5:
                continue
                
            # Clean the section text
            clean_text = clean_section_text(section_text)
            
            # Create chunks with metadata
            section_chunks = create_chunks_with_metadata(
                section_name, 
                clean_text, 
                metadata,
                MAX_CHUNK_SIZE
            )
            
            file_chunks.extend(section_chunks)
        
        return {
            "status": "success",
            "filename": filename,
            "chunks": file_chunks,
            "metadata": metadata
        }
    
    except Exception as e:
        error_details = traceback.format_exc()
        return {
            "status": "error",
            "filename": os.path.basename(pdf_path),
            "error": str(e),
            "details": error_details
        }

def process_directory(
    directory: str, 
    output_file: str, 
    workers: int = 4, 
    resume: bool = False, 
    pattern: Optional[str] = None, 
    verbose: bool = False
) -> Tuple[int, int, float]:
    """
    Process all PDF files in a directory with parallel processing.
    
    Args:
        directory: Directory containing PDF files
        output_file: Path to output JSONL file
        workers: Number of parallel workers
        resume: Whether to resume from previous run
        pattern: Optional regex pattern to filter files
        verbose: Whether to output verbose processing details
        
    Returns:
        Tuple containing:
        - Number of files processed
        - Number of chunks created
        - Processing duration in seconds
    """
    start_time = time.time()
    all_chunks = []
    errors = []
    
    # Set up logging
    logger = logging.getLogger("kswc_processor")
    
    # Check for resuming and get already processed files
    processed_files = set()
    if resume:
        processed_files = get_processed_files(output_file)
        if verbose:
            logger.info(f"Resuming processing. {len(processed_files)} files already processed.")
    
    # Get list of files to process
    pdf_files = find_pdf_files(directory, pattern)
    pdf_files = [f for f in pdf_files if os.path.basename(f) not in processed_files]
    
    if not pdf_files:
        logger.info("No new files to process.")
        return 0, 0, 0
    
    logger.info(f"Processing {len(pdf_files)} PDF files with {workers} parallel workers...")
    
    # Create log file to store detailed errors
    log_file = f"{output_file}.log"
    
    # Process files in parallel
    with ProcessPoolExecutor(max_workers=workers) as executor:
        results = list(tqdm.tqdm(
            executor.map(process_pdf_file, pdf_files), 
            total=len(pdf_files),
            desc="Processing PDFs"
        ))
    
    # Process results
    successful_files = 0
    for result in results:
        if result["status"] == "success":
            all_chunks.extend(result["chunks"])
            successful_files += 1
            if verbose:
                logger.info(
                    f"Processed {result['filename']} - "
                    f"Claimant: {result['metadata']['claimant_name']}, "
                    f"Docket: {result['metadata']['docket_number']}, "
                    f"Chunks: {len(result['chunks'])}"
                )
        else:
            errors.append(result)
            logger.error(f"Error processing {result['filename']}: {result['error']}")
            # Write detailed error to log
            with open(log_file, "a") as log:
                log.write(f"\n--- Error processing {result['filename']} ---\n")
                log.write(result["details"])
                log.write("\n-----------------------\n")
    
    # Write all chunks to JSONL
    write_chunks_to_jsonl(all_chunks, output_file, append=resume)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Log summary
    logger.info(f"Processing complete!")
    logger.info(f"Total chunks written: {len(all_chunks)}")
    logger.info(f"Total files processed successfully: {successful_files}/{len(pdf_files)}")
    logger.info(f"Files with errors: {len(errors)}")
    logger.info(f"Duration: {duration:.2f} seconds ({duration/60:.2f} minutes)")
    
    return len(pdf_files), len(all_chunks), duration

def process_single_file(file_path: str, output_file: str) -> Optional[Dict[str, Any]]:
    """
    Process a single PDF file and save chunks to JSONL.
    
    Args:
        file_path: Path to the PDF file
        output_file: Path to output JSONL file
        
    Returns:
        Processing result dictionary or None if file doesn't exist
    """
    logger = logging.getLogger("kswc_processor")
    
    if not os.path.exists(file_path):
        logger.error(f"Error: File {file_path} does not exist.")
        return None
        
    logger.info(f"Processing single file: {file_path}")
    
    result = process_pdf_file(file_path)
    
    if result["status"] == "success":
        write_chunks_to_jsonl(result["chunks"], output_file)
        logger.info(f"Successfully processed {result['filename']} - Generated {len(result['chunks'])} chunks")
    else:
        logger.error(f"Error processing {result['filename']}: {result['error']}")
        # Write detailed error to log
        with open(f"{output_file}.log", "a") as log:
            log.write(f"\n--- Error processing {result['filename']} ---\n")
            log.write(result["details"])
            log.write("\n-----------------------\n")
    
    return result 