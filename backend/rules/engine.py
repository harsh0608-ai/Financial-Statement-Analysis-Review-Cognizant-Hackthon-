"""Rule engine orchestration.

Each check is independently invoked and isolated: a failure in one check
is logged and does not prevent the other checks from running (e.g. a
grammar-check failure must not stop mathematical checks -- see
rules/spell_grammar_check.py and _run_safely below).
"""

import logging

from rules.math_check import run_math_check
from rules.consistency_check import run_consistency_check
from rules.tie_out_check import run_tie_out_check
from rules.spell_grammar_check import run_spell_grammar_check
from rules.analytical_check import run_analytical_check
from rules.ratio_check import run_ratio_check
from rules.wp514_check import run_wp514_check
from rules.optional_disclosure_check import run_optional_disclosure_check

logger = logging.getLogger(__name__)


def _run_safely(check_name: str, func, *args, **kwargs) -> list:
    try:
        return func(*args, **kwargs) or []
    except Exception:
        logger.exception("Check '%s' failed; continuing with remaining checks.", check_name)
        return []


def run_all_checks(
    line_items: list,
    pages_text: list,
    prior_statement_items: list = None,
    analytical_threshold_percent: float = None,
    include_optional_checks: bool = True,
) -> list[dict]:
    math_findings = _run_safely("mathematical_accuracy", run_math_check, line_items)
    tie_out_findings = _run_safely(
        "prior_year_tie_out", run_tie_out_check, line_items, prior_statement_items or [],
    )
    consistency_findings = _run_safely("internal_consistency", run_consistency_check, line_items)
    grammar_findings = _run_safely("spell_grammar", run_spell_grammar_check, pages_text)
    analytical_findings = _run_safely(
        "analytical_review", run_analytical_check, line_items, analytical_threshold_percent,
    )
    ratio_findings = _run_safely("ratio_analysis", run_ratio_check, line_items)

    detected_statement_types = {item.statement_type for item in line_items}
    wp514_findings = _run_safely(
        "wp514_checklist", run_wp514_check, pages_text,
        math_findings, tie_out_findings, consistency_findings, grammar_findings,
        detected_statement_types,
    )

    findings = []
    findings.extend(math_findings)
    findings.extend(tie_out_findings)
    findings.extend(consistency_findings)
    findings.extend(grammar_findings)
    findings.extend(analytical_findings)
    findings.extend(ratio_findings)
    findings.extend(wp514_findings)

    if include_optional_checks:
        findings.extend(
            _run_safely("optional_disclosure_presence", run_optional_disclosure_check, pages_text)
        )

    return findings
