import pdfplumber


def extract_raw_content(filepath: str) -> dict:
    pages_text = []
    pages_tables = []

    with pdfplumber.open(filepath) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            tables = page.extract_tables() or []
            pages_text.append({"page_number": page_number, "text": text})
            pages_tables.append({"page_number": page_number, "tables": tables})

    return {"pages_text": pages_text, "pages_tables": pages_tables}
