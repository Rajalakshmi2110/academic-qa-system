import os
import json
from extract_pdf import extract_pdf_text
from clean_text import clean_text
from chunk_text import chunk_text

PDF_PATH = r"D:\final year project\project\academic-qa\data\raw\textbooks\stallings\Data and Computer Communications by William Stallings.pdf"

def run():
    pages = extract_pdf_text(PDF_PATH)
    all_chunks = []

    for page in pages:
        cleaned = clean_text(page["text"])
        chunks = chunk_text(cleaned)

        for chunk in chunks:
            all_chunks.append({
                "unit": "Unit 1",
                "topic": "Introduction to Computer Networks",
                "source": "Stallings",
                "page": page["page"],
                "text": chunk
            })

    os.makedirs("data/processed/chunks", exist_ok=True)

    with open("data/processed/chunks/stallings_u1.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print("✔ stallings_u1.json generated successfully")

if __name__ == "__main__":
    run()
