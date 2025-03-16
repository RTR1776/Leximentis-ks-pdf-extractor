"""
Main module with CLI interface for the Kansas Workers' Compensation processor.
"""
import os
import argparse
import logging
import sys

from kswc_processor.processors import process_directory, process_single_file
from kswc_processor.utils import find_pdf_files, setup_logging
from kswc_processor.config import DEFAULT_WORKERS

def list_pdf_files(directory: str, pattern: str = None) -> None:
    """
    List PDF files in directory, optionally filtering by pattern.
    
    Args:
        directory: Directory to list files from
        pattern: Optional regex pattern to filter files
    """
    pdf_files = find_pdf_files(directory, pattern)
    
    if not pdf_files:
        print(f"No PDF files found in {directory}" +
              (f" matching pattern {pattern}" if pattern else ""))
        return
    
    print(f"Found {len(pdf_files)} PDF files" +
          (f" matching pattern {pattern}" if pattern else "") + ":")
    
    for filename in sorted([os.path.basename(f) for f in pdf_files]):
        print(f"  - {filename}")

def main() -> None:
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description='Process workers compensation PDF documents in parallel.'
    )
    
    parser.add_argument(
        '--directory', '-d', type=str,
        default=r'H:\My Drive\Kansas Workers Compensation Data\KS WC Appeal Decisions',
        help='Directory containing PDF files to process'
    )
    parser.add_argument(
        '--output', '-o', type=str,
        default="workers_comp_chunks.jsonl",
        help='Output JSONL file'
    )
    parser.add_argument(
        '--workers', '-w', type=int, default=DEFAULT_WORKERS,
        help='Number of parallel workers'
    )
    parser.add_argument(
        '--resume', '-r', action='store_true',
        help='Resume from previous run'
    )
    parser.add_argument(
        '--list', '-l', action='store_true',
        help='List PDF files in directory instead of processing'
    )
    parser.add_argument(
        '--pattern', '-p', type=str, default=None,
        help='Regex pattern to filter PDF files'
    )
    parser.add_argument(
        '--file', '-f', type=str, default=None,
        help='Process a single specific PDF file'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Set up logging
    logger = setup_logging(args.output)
    
    # Process based on arguments
    try:
        # Just list files if requested
        if args.list:
            list_pdf_files(args.directory, args.pattern)
        # Process a single file if specified
        elif args.file:
            file_path = args.file if os.path.exists(args.file) else os.path.join(args.directory, args.file)
            process_single_file(file_path, args.output)
        # Process directory
        else:
            process_directory(
                args.directory, 
                args.output,
                workers=args.workers,
                resume=args.resume,
                pattern=args.pattern,
                verbose=args.verbose
            )
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 