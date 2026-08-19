from pathlib import Path
from typing import Iterable

from knowledge_base.wp514.verified_content import WP514_SECTIONS


def load_wp514_sections() -> list[dict]:
    """Load the mentor-verified WP-514 sections shipped with the service."""
    return [dict(section) for section in WP514_SECTIONS]


def load_text_file(path: str | Path, *, source: str | None = None, topic: str = "wp514_general") -> list[dict]:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    return [{
        "section_id": p.stem,
        "title": p.stem,
        "content": text,
        "topic": topic,
        "page": None,
        "source": source or p.name,
    }]


def load_directory(path: str | Path, extensions: Iterable[str] = (".txt", ".md")) -> list[dict]:
    root = Path(path)
    sections: list[dict] = []
    allowed = {e.lower() for e in extensions}
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.suffix.lower() in allowed:
            sections.extend(load_text_file(p))
    return sections
