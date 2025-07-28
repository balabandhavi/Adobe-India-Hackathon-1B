# Challenge 1b: Multi-Collection PDF Analysis

This repository contains a solution for Challenge 1b of the Adobe India Hackathon. It processes multiple document collections based on user personas and outputs structured summaries in a defined JSON format.

## Project Structure

```
adobe-challenge-1b/
├── sample_dataset/
│   ├── Collection 1/
│   │   ├── PDFs/
│   │   ├── challenge1b_input1.json
│   │   └── challenge1b_output1.json (generated)
│   ├── Collection 2/
│   │   └── ...
│   └── Collection 3/
│       └── ...
├── process_pdfs.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## How to Run the Code

### Option 1: Run Locally (Python)

#### 1. Install dependencies:

```
pip install -r requirements.txt
```

#### 2. Prepare your collections under `sample_dataset/`

Each collection folder should include:

* A `PDFs/` subfolder containing documents
* A `challenge1b_input*.json` input file (name can vary)

#### 3. Run the script:

```
python process_pdfs.py --input_base sample_dataset
```

This will generate corresponding `challenge1b_output*.json` files in each collection folder.

---

### Option 2: Run via Docker

#### 1. Build the Docker image:

```
docker build -t pdf-analyzer .
```

#### 2. Run the container:

```
docker run --rm \
  -v $(pwd)/sample_dataset:/app/sample_dataset \
  pdf-analyzer
```

Note: Replace `$(pwd)` with the absolute path if running on Windows CMD or PowerShell.

---

## Output Format

Each output JSON follows the structure:

```
{
  "metadata": {
    "input_documents": [...],
    "persona": "...",
    "job_to_be_done": "...",
    "processing_timestamp": "..."
  },
  "extracted_sections": [...],
  "subsection_analysis": [...]
}
```

## Dependencies

* Python 3.10+
* PyMuPDF

## Notes

* Script automatically handles any number of collections.
* Input JSON must follow the expected schema.
* Output JSON is written next to the input JSON in each collection folder.

## License

This solution is provided as-is for the Adobe Hackathon Challenge.
