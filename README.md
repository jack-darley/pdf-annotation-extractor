# PDF Highlight Extractor

A Python tool that extracts highlighted text from PDF files in a folder, cleans the text, and exports the results to a CSV file.

## What it does
- Scans a directory for `.pdf` files  
- Extracts highlight annotations from each PDF  
- Cleans extracted text (removes OCR artifacts, broken words, and control characters)  
- Outputs one row per highlight for easy analysis  

## Output format

The CSV contains:
- `Filename`: Name of the PDF file  
- `Page`: Page number where the highlight appears  
- `Annotation`: Cleaned highlight text  

## Requirements

Install dependencies:

```bash
pip install pymupdf pandas
```

## Usage

Run the script from the terminal:

```bash

python main.py /path/to/input/folder /path/to/output/filename