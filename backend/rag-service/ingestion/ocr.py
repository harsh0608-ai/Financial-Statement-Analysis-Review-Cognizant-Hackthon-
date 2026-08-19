from pathlib import Path


def ocr_image(path: str | Path) -> str:
    """OCR helper for future/source-document ingestion.

    The shipped WP-514 knowledge base uses mentor-verified text rather than
    blindly trusting OCR because the source photographs contain glare/skew.
    """
    try:
        import pytesseract
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Install pytesseract and Pillow to use OCR") from exc

    return pytesseract.image_to_string(Image.open(path))
