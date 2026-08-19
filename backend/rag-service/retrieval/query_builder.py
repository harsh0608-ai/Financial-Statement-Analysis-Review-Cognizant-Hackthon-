from __future__ import annotations

CHECK_TOPIC = {
    "mathematical_accuracy": "mathematical_accuracy",
    "prior_year_tie_out": "prior_year_consistency",
    "internal_consistency": "internal_consistency",
    "spell_grammar": "spell_grammar",
    "analytical_review": "planning_analytics",
    "ratio_analysis": "ratio_analysis",
    "wp514_checklist": "wp514_general",
    "optional_disclosure_presence": "wp514_general",
}


def topic_for_check(check_type: str) -> str:
    return CHECK_TOPIC.get(check_type, "wp514_general")


def build_query(finding) -> str:
    check_type = finding.check_type
    topic = topic_for_check(check_type)
    parts = ["WP-514", topic.replace("_", " "), check_type.replace("_", " ")]
    for value in (finding.location, finding.description):
        if value:
            parts.append(str(value))
    if finding.current_year_value is not None and finding.prior_year_value is not None:
        parts.append("current year versus prior year comparison")
    if finding.reported_value is not None and finding.expected_value is not None:
        parts.append("recalculation expected versus reported value")
    return " ".join(parts)
