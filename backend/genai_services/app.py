from fastapi import FastAPI, HTTPException

from generator import generate_review_explanation
from schemas import GenAIRequest


app = FastAPI(
    title="Financial Statement GenAI Service",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "genai",
    }


@app.post("/explain")
def explain(request: GenAIRequest):

    try:
        result = generate_review_explanation(
            finding=request.finding,
            contexts=request.contexts,
        )

        return result.model_dump()

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"GenAI generation failed: {str(exc)}",
        )