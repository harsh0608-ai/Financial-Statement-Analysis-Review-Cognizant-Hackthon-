from __future__ import annotations

import re
from typing import Iterable


def _words(text: str) -> list[str]:
    return re.findall(r"\S+", text.strip())


def chunk_sections(sections: Iterable[dict], chunk_size: int = 500, overlap: int = 50) -> list[dict]:
    """Chunk logical sections while preserving section/example metadata.

    If a section fits, it remains intact. Large sections are split by paragraph
    boundaries first, then by words as a last resort. Formula/example text is
    therefore kept together whenever possible.
    """
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("chunk_size must be > 0 and 0 <= overlap < chunk_size")

    chunks: list[dict] = []
    for section in sections:
        text = str(section.get("content", "")).strip()
        if not text:
            continue
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        pieces: list[str] = []
        current: list[str] = []
        count = 0

        for para in paragraphs:
            n = len(_words(para))
            if current and count + n > chunk_size:
                pieces.append("\n\n".join(current))
                current = []
                count = 0
            if n <= chunk_size:
                current.append(para)
                count += n
            else:
                words = _words(para)
                start = 0
                while start < len(words):
                    end = min(start + chunk_size, len(words))
                    pieces.append(" ".join(words[start:end]))
                    start = end - overlap if end < len(words) else end
                current = []
                count = 0
        if current:
            pieces.append("\n\n".join(current))

        for idx, piece in enumerate(pieces):
            chunks.append({
                "id": f"{section['section_id']}-{idx}",
                "text": f"{section.get('title', '')}\n\n{piece}".strip(),
                "metadata": {
                    "section_id": section["section_id"],
                    "title": section.get("title", ""),
                    "topic": section.get("topic", "wp514_general"),
                    "page": section.get("page"),
                    "source": section.get("source", "WP514_mentor_reference"),
                    "document_type": "wp514",
                    "chunk_index": idx,
                },
            })
    return chunks
