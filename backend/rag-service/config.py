"""
RAG Service Configuration.

All settings are read from environment variables with sensible defaults.
No mandatory API keys — the service runs fully locally.
"""

import os
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
VECTOR_STORE_PATH = os.getenv(
    "VECTOR_STORE_PATH",
    str(BASE_DIR / "data" / "vector_store"),
)
KNOWLEDGE_BASE_DIR = os.getenv(
    "KNOWLEDGE_BASE_DIR",
    str(BASE_DIR / "knowledge_base" / "wp514"),
)

# ── Embedding model ──────────────────────────────────────────────────────
# all-MiniLM-L6-v2: 384-dim, 80 MB, fast, strong STS performance.
# Runs locally via sentence-transformers — no API key required.
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# ── Chunking ─────────────────────────────────────────────────────────────
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

# ── Retrieval ────────────────────────────────────────────────────────────
TOP_K = int(os.getenv("TOP_K", "5"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.25"))

# ── Server ───────────────────────────────────────────────────────────────
HOST = os.getenv("RAG_HOST", "0.0.0.0")
PORT = int(os.getenv("RAG_PORT", "8001"))

# ── ChromaDB collection name ─────────────────────────────────────────────
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "wp514_knowledge")
