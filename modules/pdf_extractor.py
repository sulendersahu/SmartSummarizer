import fitz  # PyMuPDF

def extract_pdf_text(pdf_bytes: bytes) -> str:
    """Extract selectable text from an in-memory PDF."""
    document = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    try:
        for page in document:
            page_text = page.get_text("text")
            if page_text:
                pages.append(page_text)
    finally:
        document.close()
    return "\n\n".join(pages).strip()
