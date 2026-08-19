from __future__ import annotations

from pathlib import Path

import chromadb

from config import COLLECTION_NAME, VECTOR_STORE_PATH
from ingestion.metadata import normalize_metadata


class VectorStore:
    def __init__(self, path: str = VECTOR_STORE_PATH, collection_name: str = COLLECTION_NAME):
        Path(path).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def reset(self) -> None:
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    def upsert(self, chunks: list[dict], embeddings: list[list[float]]) -> None:
        if not chunks:
            return
        self.collection.upsert(
            ids=[c["id"] for c in chunks],
            documents=[c["text"] for c in chunks],
            embeddings=embeddings,
            metadatas=[normalize_metadata(c["metadata"]) for c in chunks],
        )

    def count(self) -> int:
        return self.collection.count()

    def query(self, embedding: list[float], top_k: int = 5, where: dict | None = None) -> list[dict]:
        kwargs = {
            "query_embeddings": [embedding],
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            kwargs["where"] = where
        result = self.collection.query(**kwargs)
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        rows = []
        for doc, meta, distance in zip(docs, metas, distances):
            # Chroma cosine distance is approximately 1 - cosine similarity.
            score = max(0.0, min(1.0, 1.0 - float(distance)))
            rows.append({"text": doc, "metadata": meta or {}, "score": score})
        return rows
