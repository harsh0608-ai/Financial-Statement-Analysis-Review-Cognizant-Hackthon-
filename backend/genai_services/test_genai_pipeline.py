from generator import generate_review_explanation
from schemas import FinancialFinding, RAGContext


# --------------------------------------------------
# TEST FINDING
# This represents a finding produced by the Rule Engine.
# --------------------------------------------------

finding = FinancialFinding(
    id=53,
    check_type="mathematical_accuracy",
    location="WP-514",
    severity="medium",
    description=(
        "Potential mathematical accuracy issue identified. "
        "Relevant totals or arithmetic relationships should be recalculated."
    ),
    reported_value=None,
    expected_value=None,
    difference=None,
    current_year_value=None,
    prior_year_value=None,
    percentage_change=None,
    threshold=None,
    page_number=1,
    evidence=[],
)


# --------------------------------------------------
# RAG CONTEXT
# This is the structured response received from your
# teammate's RAG service.
# --------------------------------------------------

contexts = [
    RAGContext(
        text=(
            "Mathematical Accuracy — WP-514 Guidance\n\n"
            "Mathematical Accuracy Review\n\n"
            "What it involves: Recalculate totals, subtotals, "
            "cross-casts, earnings, cash-flow movements, note totals, "
            "and other arithmetic relationships.\n\n"
            "Expected evidence/output: Evidence that formulas, "
            "additions, and cross-references are accurate."
        ),
        source="WP514_mentor_reference",
        page=1,
        topic="mathematical_accuracy",
        score=0.6568,
    ),
    RAGContext(
        text=(
            "Example 9: Internal Consistency Review\n\n"
            "Check that Revenue in Income Statement agrees with Revenue Note..."
        ),
        source="WP514_mentor_reference",
        page=3,
        topic="internal_consistency",
        score=0.5169,
    ),
]


# --------------------------------------------------
# CALL GENAI
# --------------------------------------------------

print("\nSending finding + RAG context to Gemini...\n")

result = generate_review_explanation(
    finding=finding,
    contexts=contexts,
)


# --------------------------------------------------
# DISPLAY RESULT
# --------------------------------------------------

print("=" * 60)
print("GENAI RESULT")
print("=" * 60)

print("\nFinding ID:")
print(result.finding_id)

print("\nStatus:")
print(result.status)

print("\nSeverity:")
print(result.severity)

print("\nExplanation:")
print(result.explanation)

print("\nWP-514 Relevance:")
print(result.wp514_relevance)

print("\nRecommended Action:")
print(result.recommended_action)

print("\nSources:")
for source in result.sources:
    print(
        f"- {source.source} | "
        f"Page: {source.page} | "
        f"Topic: {source.topic}"
    )

print("\n" + "=" * 60)
print("GENAI PIPELINE TEST PASSED")
print("=" * 60)