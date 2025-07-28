import json
from datetime import datetime
from pathlib import Path
import fitz  # PyMuPDF
import argparse

# Parse command-line args
parser = argparse.ArgumentParser()
parser.add_argument("--input_base", type=str, default="sample_dataset", help="Base input folder path")
args = parser.parse_args()

base_path = Path(args.input_base)

# Function to extract sample text block
def extract_first_text_block(pdf_path, max_chars=1000):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(min(3, len(doc))):
        text += doc[page_num].get_text()
        if len(text) >= max_chars:
            break
    return text.strip()[:max_chars], 1

# Loop through all Collection folders dynamically
for collection_dir in base_path.glob("Collection*"):
    input_jsons = list(collection_dir.glob("challenge1b_input*.json"))
    if not input_jsons:
        print(f"No input JSON found in {collection_dir.name}, skipping.")
        continue

    input_path = input_jsons[0]
    with open(input_path) as f:
        input_data = json.load(f)

    output = {
        "metadata": {
            "input_documents": [],
            "persona": input_data["persona"]["role"],
            "job_to_be_done": input_data["job_to_be_done"]["task"],
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for idx, doc in enumerate(input_data["documents"], start=1):
        filename = doc["filename"]
        title = doc.get("title", "Unknown Title")
        file_path = collection_dir / "PDFs" / filename

        if not file_path.exists():
            print(f"Skipping missing file: {filename}")
            continue

        output["metadata"]["input_documents"].append(filename)

        text_block, page_number = extract_first_text_block(file_path)

        output["extracted_sections"].append({
            "document": filename,
            "section_title": title,
            "importance_rank": idx,
            "page_number": page_number
        })

        output["subsection_analysis"].append({
            "document": filename,
            "refined_text": text_block,
            "page_number": page_number
        })

    # Save result using matching output name
    output_filename = input_path.name.replace("input", "output")
    output_path = collection_dir / output_filename
    with open(output_path, "w") as out_f:
        json.dump(output, out_f, indent=2)

    print(f"Saved {output_filename} to {collection_dir}")
