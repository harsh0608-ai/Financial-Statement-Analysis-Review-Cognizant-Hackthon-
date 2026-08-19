from pydantic import BaseModel, Field


class RAGContext(BaseModel):
    text: str
    source: str
    page: int | None = None
    topic: str
    score: float


class FinancialFinding(BaseModel):
    id: int
    check_type: str
    location: str
    severity: str
    description: str

    reported_value: float | None = None
    expected_value: float | None = None
    difference: float | None = None

    current_year_value: float | None = None
    prior_year_value: float | None = None
    percentage_change: float | None = None
    threshold: float | None = None

    page_number: int | None = None
    evidence: list[dict] = []


class GenAIRequest(BaseModel):
    finding: FinancialFinding
    contexts: list[RAGContext]


class SourceReference(BaseModel):
    source: str
    page: int | None = None
    topic: str


class ReviewExplanation(BaseModel):
    finding_id: int

    status: str

    explanation: str

    wp514_relevance: str

    recommended_action: str

    severity: str

    sources: list[SourceReference]