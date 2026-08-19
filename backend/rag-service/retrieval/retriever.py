from __future__ import annotations

from config import SIMILARITY_THRESHOLD, TOP_K
from embeddings.embedder import LocalEmbedder
from retrieval.query_builder import build_query, topic_for_check
from retrieval.reranker import rerank
from vector_store.store import VectorStore


class Retriever:
    def __init__(self, embedder: LocalEmbedder | None = None, store: VectorStore | None = None):
        self.embedder = embedder or LocalEmbedder()
        self.store = store or VectorStore()

    def retrieve(self, finding, top_k: int = TOP_K, threshold: float = SIMILARITY_THRESHOLD) -> dict:
        query = build_query(finding)
        embedding = self.embedder.encode([query])[0]
        preferred_topic = topic_for_check(finding.check_type)

        # Search preferred topic first, then fall back to all WP-514 knowledge
        # if too few useful results are found.
        rows = self.store.query(embedding, top_k=top_k, where={"topic": preferred_topic})
        rows = rerank(rows, query, preferred_topic)
        rows = [r for r in rows if r["score"] >= threshold]

        if len(rows) < min(2, top_k):
            fallback = self.store.query(embedding, top_k=top_k)
            fallback = rerank(fallback, query, preferred_topic)
            seen = {r["text"] for r in rows}
            for row in fallback:
                if row["text"] not in seen and row["score"] >= threshold:
                    rows.append(row)
                    seen.add(row["text"])
                if len(rows) >= top_k:
                    break

        rows = sorted(rows, key=lambda r: r["score"], reverse=True)[:top_k]
        return {"query": query, "rows": rows}
