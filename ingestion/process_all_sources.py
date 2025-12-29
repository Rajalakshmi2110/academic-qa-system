import os
import json
import re
from extract_pdf import extract_pdf_text
from clean_text import clean_text
from chunk_text import chunk_text
from pptx import Presentation
import nltk

nltk.download("punkt", quiet=True)

# ==============================
# UNIT MAPS
# ==============================

STALLINGS_UNIT_MAP = {
    1: "Unit 1", 2: "Unit 1",
    3: "Unit 2", 4: "Unit 2",
    5: "Unit 3", 6: "Unit 3",
    7: "Unit 4", 8: "Unit 4",
    9: "Unit 5"
}

KUROSE_UNIT_MAP = {
    1: "Unit 1", 2: "Unit 1",
    3: "Unit 2", 4: "Unit 2",
    5: "Unit 3",
    6: "Unit 4", 7: "Unit 4",
    8: "Unit 5"
}

# ==============================
# CONFIG
# ==============================

RAW_DIR = "data/raw"
OUTPUT_DIR = "data/processed/chunks"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SKIP_KEYWORDS = [
    "edition", "copyright", "pearson",
    "table of contents", "preface",
    "associated companies", "global edition"
]

# ==============================
# HELPERS
# ==============================

def infer_chapter_from_section(text):
    match = re.search(r"\b(\d+)\.\d+\b", text)
    return int(match.group(1)) if match else None


def extract_chapter_number(text):
    match = re.search(r"\bchapter\s+(\d+)\b", text, re.IGNORECASE)
    return int(match.group(1)) if match else None


def get_unit_from_chapter(chapter, book_type):
    if book_type == "stallings":
        return STALLINGS_UNIT_MAP.get(chapter, "Unknown")
    if book_type == "kurose":
        return KUROSE_UNIT_MAP.get(chapter, "Unknown")
    return "Unknown"


# ==============================
# PDF PROCESSOR (TEXTBOOKS)
# ==============================

def process_pdf_file(file_path, book_type):
    pages = extract_pdf_text(file_path)
    all_chunks = []

    current_unit = "Unknown"

    for page in pages:
        raw = page["text"].lower()
        if any(k in raw for k in SKIP_KEYWORDS):
            continue

        chapter = extract_chapter_number(page["text"])

        if not chapter:
            chapter = infer_chapter_from_section(page["text"])

        if chapter:
            current_unit = get_unit_from_chapter(chapter, book_type)


        cleaned = clean_text(page["text"])
        chunks = chunk_text(cleaned)

        for chunk in chunks:
            all_chunks.append({
                "unit": current_unit,
                "topic": f"Chapter {chapter}" if chapter else "General",
                "source": book_type,
                "page": page["page"],
                "text": chunk
            })

    return all_chunks


# ==============================
# NOTES
# ==============================

def process_notes_folder(notes_folder):
    all_chunks = []

    for pdf in os.listdir(notes_folder):
        if not pdf.lower().endswith(".pdf"):
            continue

        path = os.path.join(notes_folder, pdf)
        match = re.search(r"unit\s*(\d+)", pdf, re.IGNORECASE)
        unit = f"Unit {match.group(1)}" if match else "Unknown"

        pages = extract_pdf_text(path)

        for page in pages:
            cleaned = clean_text(page["text"])
            chunks = chunk_text(cleaned)

            for chunk in chunks:
                all_chunks.append({
                    "unit": unit,
                    "topic": "Notes",
                    "source": "notes",
                    "page": page["page"],
                    "text": chunk
                })

    return all_chunks


# ==============================
# PPTs
# ==============================

def process_ppts_folder(ppt_folder):
    all_chunks = []

    for file in os.listdir(ppt_folder):
        path = os.path.join(ppt_folder, file)
        match = re.search(r"unit\s*(\d+)", file, re.IGNORECASE)
        unit = f"Unit {match.group(1)}" if match else "Unknown"

        # PDF slides
        if file.lower().endswith(".pdf"):
            pages = extract_pdf_text(path)
            for page in pages:
                cleaned = clean_text(page["text"])
                chunks = chunk_text(cleaned)

                for chunk in chunks:
                    all_chunks.append({
                        "unit": unit,
                        "topic": "Slide",
                        "source": "ppt",
                        "page": page["page"],
                        "text": chunk
                    })

        # PPTX
        elif file.lower().endswith(".pptx"):
            prs = Presentation(path)
            for i, slide in enumerate(prs.slides):
                text = []
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text.append(shape.text)

                slide_text = "\n".join(text).strip()
                if slide_text:
                    all_chunks.append({
                        "unit": unit,
                        "topic": "Slide",
                        "source": "ppt",
                        "page": i + 1,
                        "text": slide_text
                    })

    return all_chunks


# ==============================
# SYLLABUS
# ==============================

def process_syllabus_file(file_path, units):
    pages = extract_pdf_text(file_path)
    syllabus_json = []

    pages_per_unit = max(1, len(pages) // len(units))

    for idx, page in enumerate(pages):
        unit = units[min(idx // pages_per_unit, len(units) - 1)]
        text = clean_text(page["text"])
        topics = [t.strip() for t in text.split("\n") if t.strip()]

        syllabus_json.append({
            "unit": unit,
            "topics": topics
        })

    out = os.path.join(OUTPUT_DIR, "syllabus.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(syllabus_json, f, indent=2, ensure_ascii=False)

    print(f"✔ Syllabus processed → {out}")


# ==============================
# MAIN
# ==============================

all_chunks = []

# 📘 TEXTBOOKS
textbooks_dir = os.path.join(RAW_DIR, "textbooks")
for book in os.listdir(textbooks_dir):
    book_type = "stallings" if "stallings" in book.lower() else "kurose"
    book_path = os.path.join(textbooks_dir, book)

    for pdf in os.listdir(book_path):
        if pdf.lower().endswith(".pdf"):
            all_chunks.extend(process_pdf_file(os.path.join(book_path, pdf), book_type))

print(f"✔ Textbooks processed: {len(all_chunks)} chunks")

# 📝 NOTES
all_chunks.extend(process_notes_folder(os.path.join(RAW_DIR, "notes")))
print(f"✔ Notes processed: {len(all_chunks)} chunks")

# 📊 PPTs
all_chunks.extend(process_ppts_folder(os.path.join(RAW_DIR, "ppts")))
print(f"✔ PPTs processed: {len(all_chunks)} chunks")

# 💾 SAVE
out = os.path.join(OUTPUT_DIR, "all_chunks.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2, ensure_ascii=False)

print(f"✔ All chunks saved → {out}")

# 📑 SYLLABUS
syllabus_file = os.path.join(RAW_DIR, "syllabus", "syllabus.pdf")
process_syllabus_file(syllabus_file, ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5"])
