from __future__ import annotations

from fastapi import FastAPI, HTTPException

from config import EMBEDDING_MODEL, TOP_K
from embeddings.embedder import LocalEmbedder
from retrieval.retriever import Retriever
from schemas.api_models import (
    ContextResult,
    FindingRetrievalResult,
    HealthResponse,
    RetrieveRequest,
    RetrieveResponse,
)
from vector_store.store import VectorStore

app = FastAPI(title="Financial Statement WP-514 RAG Service", version="1.0.0")

_store = VectorStore()
_embedder = LocalEmbedder()
_retriever = Retriever(embedder=_embedder, store=_store)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        collection_count=_store.count(),
        embedding_model=EMBEDDING_MODEL,
        message="RAG service is running",
    )


@app.post("/retrieve", response_model=RetrieveResponse)
def retrieve(request: RetrieveRequest) -> RetrieveResponse:
    if _store.count() == 0:
        raise HTTPException(status_code=503, detail="Knowledge base is empty. Run the ingestion/indexer first.")

    results = []
    for finding in request.findings:
        result = _retriever.retrieve(finding)
        contexts = [
            ContextResult(
                text=row["text"],
                source=str(row["metadata"].get("source", "unknown")),
                page=row["metadata"].get("page"),
                topic=str(row["metadata"].get("topic", "wp514_general")),
                score=round(float(row["score"]), 4),
            )
            for row in result["rows"]
        ]
        results.append(
            FindingRetrievalResult(
                finding_id=finding.id,
                query=result["query"],
                status="success" if contexts else "insufficient_context",
                contexts=contexts,
            )
        )
    return RetrieveResponse(results=results)
