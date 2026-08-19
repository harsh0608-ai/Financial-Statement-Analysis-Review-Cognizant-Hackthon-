from __future__ import annotations

from config import CHUNK_OVERLAP, CHUNK_SIZE
from embeddings.embedder import LocalEmbedder
from ingestion.chunker import chunk_sections
from ingestion.loader import load_wp514_sections
from vector_store.store import VectorStore


def build_index(reset: bool = False) -> int:
    sections = load_wp514_sections()
    chunks = chunk_sections(sections, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
    embedder = LocalEmbedder()
    vectors = embedder.encode([c["text"] for c in chunks])
    store = VectorStore()
    if reset:
        store.reset()
    store.upsert(chunks, vectors)
    return store.count()


if __name__ == "__main__":
    count = build_index(reset=True)
    print(f"Indexed {count} WP-514 chunks")
