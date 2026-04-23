import re

def clean_highlight(text):

    if not text:
        return ""
    
    # Fix broken hyphenated words across lines (e.g., "map-\nping" -> "mapping")
    text = re.sub(r'-\s*\n\s*', '', text) 
    
    # Replace newlines and non-breaking spaces with normal spaces
    text = text.replace('\n', ' ').replace('\xa0', ' ')
    
    # Remove soft hyphens
    text = text.replace('\xad', '')
    
    # Remove hex control characters (weird invisible PDF artifacts)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)
    
    # Target the "OCR Soup" (isolated 1-2 letter combinations separated by spaces)
    text = re.sub(r'(?:^|\s)(?:[a-zA-Z]{1,2}\s+){2,}[a-zA-Z]{1,2}?(?=\s|$)', ' ', text)
    
    # Target single/double floating letters at the very start of a string
    text = re.sub(r'^[a-zA-Z]{1,2}\s+', '', text)
    
    # Collapse multiple spaces into a single space and strip edges
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def main():
    import fitz
    import pandas as pd
    import os
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    parser.add_argument("output_path")
    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path

    all_annots = []
    for filename in os.listdir(input_path):        # Loop through each pdf
        if filename.endswith(".pdf"):               # Check for pdf filetype
            filepath = os.path.join(input_path, filename)
            doc = fitz.open(filepath)               # Open file and store in doc variable

            # print(f"\n--- {filename} ---")          # Print name of file

            for page_number, page in enumerate(doc):
                annotations = page.annots()
                if not annotations:
                    continue

                for annot in annotations:
                    if annot.type[0] == 8:
                        raw_text = page.get_text("text", clip=annot.rect)
                        cleaned_text = clean_highlight(raw_text)

                        if cleaned_text:
                            all_annots.append({
                                "Filename": filename,
                                "Page": page_number + 1,
                                "Annotation": cleaned_text
                            })
    # Save annotations for all files to csv
    pd.DataFrame(all_annots).to_csv(f"{output_path}.csv", index=False)

if __name__ == "__main__":
    main()