import fitz  # PyMuPDF

def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []

    for page_num, page in enumerate(doc):
        text = page.get_text("text")
        pages.append({
            "page": page_num + 1,
            "text": text
        })

    return pages
