# Academic QA System

Document ingestion and processing system for Computer Networks course materials.

## Structure
- `ingestion/` - Text extraction and processing pipeline
- `data/processed/chunks/` - Structured JSON output
- `data/raw/` - Source materials (PDFs, PPTs)

## Usage
```bash
pip install -r requirements.txt
python ingestion/process_all_sources.py
```

## Output Format
Organized chunks with metadata: unit, topic, source, page, text