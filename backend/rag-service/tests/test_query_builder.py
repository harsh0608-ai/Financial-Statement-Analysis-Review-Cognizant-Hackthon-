from schemas.api_models import FindingInput
from retrieval.query_builder import build_query, topic_for_check


def test_topic_mapping():
    assert topic_for_check("prior_year_tie_out") == "prior_year_consistency"
    assert topic_for_check("analytical_review") == "planning_analytics"


def test_query_contains_finding_details():
    finding = FindingInput(
        id=1,
        check_type="mathematical_accuracy",
        location="Balance Sheet / Total Assets",
        description="Reported total differs from calculated total",
    )
    q = build_query(finding)
    assert "mathematical accuracy" in q
    assert "Total Assets" in q
    assert "Reported total" in q
