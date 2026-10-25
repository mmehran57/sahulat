import json
import re
from pathlib import Path
from pypdf import PdfReader

def clean_text(text: str) -> str:
    """Collapses runs of spaces and blank lines, and strips edges."""
    if not text:
        return ""
    
    # Collapse runs of spaces and tabs into a single space
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Collapse runs of multiple newlines/blank lines into a single paragraph break (\n\n)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    
    # Strip leading and trailing whitespace
    return text.strip()

# Setup paths
raw = Path("data/raw")
processed_dir = Path("data/processed")
processed_dir.mkdir(parents=True, exist_ok=True)
output_path = processed_dir / "pages.jsonl"

# Open the JSONL file once in write mode
with open(output_path, "w", encoding="utf-8") as f_out:
    for pdf_path in raw.glob("*.pdf"):
        try:
            reader = PdfReader(pdf_path)
            
            # Loop over every page, using enumerate to track the page number (1-indexed)
            for page_num, page in enumerate(reader.pages, start=1):
                raw_text = page.extract_text()
                cleaned = clean_text(raw_text)
                
                # Optionally, skip empty pages
                if cleaned:
                    record = {
                        "doc": pdf_path.name,
                        "page": page_num,
                        "text": cleaned
                    }
                    
                    # Write the JSON string followed by a newline
                    f_out.write(json.dumps(record, ensure_ascii=False) + "\n")
                    
        except Exception as e:
            print(f"Error processing {pdf_path.name}: {e}")