from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL
from prompts import build_prompt
from schemas import (
    FinancialFinding,
    RAGContext,
    ReviewExplanation,
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_review_explanation(
    finding: FinancialFinding,
    contexts: list[RAGContext],
) -> ReviewExplanation:

    prompt = build_prompt(
        finding,
        contexts,
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ReviewExplanation,
        ),
    )

    return response.parsed