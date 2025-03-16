# Kansas Workers' Compensation Document Processor

A Python tool for processing Kansas workers' compensation legal documents, extracting text, and creating logical chunks suitable for embedding and querying with language models.

## Features

- Extract text from PDF documents
- Identify document sections (APPEARANCES, FINDINGS OF FACT, etc.)
- Extract case metadata (claimant, docket number, respondent)
- Create logical, properly-sized chunks with appropriate context
- Parallel processing of multiple documents
- Resumable processing for large collections
- Filtering capability using regex patterns

## Requirements

- Python 3.10 or higher
- PyPDF2
- tqdm

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install PyPDF2 tqdm
   ```

## Usage

### Command Line

The processor can be run from the command line:

```bash
python -m kswc_processor.main --directory "path/to/pdfs" --output "output.jsonl"
```

### Options

- `--directory`, `-d`: Directory containing PDF files to process
- `--output`, `-o`: Output JSONL file
- `--workers`, `-w`: Number of parallel workers (default: 4)
- `--resume`, `-r`: Resume from previous run
- `--list`, `-l`: List PDF files in directory instead of processing
- `--pattern`, `-p`: Regex pattern to filter PDF files
- `--file`, `-f`: Process a single specific PDF file
- `--verbose`, `-v`: Enable verbose output

### Examples

List all PDF files in a directory:
```bash
python -m kswc_processor.main --directory "path/to/pdfs" --list
```

Process files matching a pattern:
```bash
python -m kswc_processor.main --directory "path/to/pdfs" --pattern "2023" --output "2023_cases.jsonl"
```

Process a single file:
```bash
python -m kswc_processor.main --file "path/to/document.pdf" --output "document_chunks.jsonl"
```

Resume a previous processing run:
```bash
python -m kswc_processor.main --directory "path/to/pdfs" --output "output.jsonl" --resume
```

## Output Format

The processor outputs a JSONL file where each line is a JSON object representing a chunk of text with metadata:

```json
{
  "text": "Case: 123,456 | Claimant: JOHN DOE\nSection: FINDINGS OF FACT\n\n[Chunk text here]",
  "metadata": {
    "docket_number": "123,456",
    "claimant_name": "JOHN DOE",
    "section": "FINDINGS OF FACT",
    "chunk_index": 0,
    "chunk_count": 3,
    "filename": "document.pdf"
  }
}
```

## Using as a Library

The processor can also be used as a library in your Python code:

```python
from kswc_processor import process_directory, process_single_file

# Process a directory of files
process_directory(
    directory="path/to/pdfs", 
    output_file="output.jsonl",
    workers=4,
    resume=False,
    pattern="2023",
    verbose=True
)

# Process a single file
process_single_file("path/to/document.pdf", "output.jsonl")
``` 