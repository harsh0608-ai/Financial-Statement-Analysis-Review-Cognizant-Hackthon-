"""
Pydantic models for the RAG API.

The FindingInput schema matches the REAL Finding schema from the existing
backend (backend/db/models.py) — every field that the rule engine populates
is accepted here so the query builder can use any available signal.
"""

from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, Field


class FindingInput(BaseModel):
    """A single finding produced by the backend rule engine.

    Mirrors the columns of backend.db.models.Finding.  Only ``check_type``
    and ``description`` are required; the rest are nullable because not every
    check populates every field.
    """

    id: Optional[int] = Field(None, description="Finding primary key")
    check_type: str = Field(..., description="Rule-engine check type identifier")
    location: Optional[str] = Field(None, description="Where in the statements the issue was found")
    severity: Optional[str] = Field("medium", description="low | medium | high | info")
    description: str = Field(..., description="Human-readable description of the finding")

    # Mathematical / consistency / tie-out fields
    reported_value: Optional[float] = None
    expected_value: Optional[float] = None
    difference: Optional[float] = None

    # Analytical review fields
    current_year_value: Optional[float] = None
    prior_year_value: Optional[float] = None
    percentage_change: Optional[float] = None
    threshold: Optional[float] = None

    page_number: Optional[int] = None
    evidence: Optional[Any] = Field(None, description="JSON list of supporting evidence items")


class RetrieveRequest(BaseModel):
    """Request body for POST /retrieve."""

    findings: list[FindingInput] = Field(..., min_length=1)


class ContextResult(BaseModel):
    """A single retrieved knowledge-base chunk."""

    text: str
    source: str
    page: Optional[int] = None
    topic: str
    score: float


class FindingRetrievalResult(BaseModel):
    """Retrieval results for one finding."""

    finding_id: Optional[int] = None
    query: str
    status: str = Field(description="'success' or 'insufficient_context'")
    contexts: list[ContextResult] = []


class RetrieveResponse(BaseModel):
    """Response body for POST /retrieve."""

    results: list[FindingRetrievalResult]


class HealthResponse(BaseModel):
    """Response body for GET /health."""

    status: str
    collection_count: int
    embedding_model: str
    message: str
