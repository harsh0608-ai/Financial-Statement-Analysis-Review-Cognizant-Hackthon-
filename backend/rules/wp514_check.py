"""WP-514 checklist.

Rebuilt directly from the mentor-provided WP-514 reference material
("Understanding the WP-514 Statement", section 5 "Suggested WP-514 review
checklist" and the matching checklist on the following page). WP-514 is a
*workpaper completeness/governance* check, not a mandatory-disclosure-
keyword scan -- it confirms that the underlying review activities
(mathematical accuracy, prior-year tie-out, internal consistency, spelling
and grammar, and required sections) were performed and clean, plus a small
number of items that are inherently manual (exception sign-off).

This module does not re-derive findings itself; it summarizes the results
of the other checks (already run by rules.engine) into checklist-style
findings, per the checklist:

  - Current-year and prior-year amounts agree to source documents
    -> prior-year tie-out results
  - Planning analytics are mathematically accurate
    -> mathematical accuracy results
  - Primary statements, notes, disclosures, cross-references are
    internally consistent -> internal consistency results
  - Spelling, grammar, headings, dates, units, formatting are consistent
    -> spelling/grammar results
  - All required WP-514 sections completed
    -> required statement sections detected
  - Exceptions resolved / preparer & reviewer sign-off
    -> flagged as a manual step (not automatable by this system)

Any prior assumption about specific "required disclosures" that is not
supported by the mentor material is intentionally NOT included here --
see rules/optional_disclosure_check.py.
"""

REQUIRED_STATEMENT_SECTIONS = {"Balance Sheet", "P&L", "Cash Flow"}


def run_wp514_check(
    pages_text: list,
    math_findings: list = None,
    tie_out_findings: list = None,
    consistency_findings: list = None,
    grammar_findings: list = None,
    detected_statement_types: set = None,
) -> list[dict]:
    math_findings = math_findings or []
    tie_out_findings = tie_out_findings or []
    consistency_findings = consistency_findings or []
    grammar_findings = grammar_findings or []
    detected_statement_types = detected_statement_types or set()

    findings = []

    findings.append(_checklist_item(
        "Mathematical accuracy",
        passed=len(math_findings) == 0,
        detail=(
            f"{len(math_findings)} mathematical accuracy exception(s) found."
            if math_findings else
            "Totals, subtotals, and cross-casts recalculated without exception."
        ),
    ))

    findings.append(_checklist_item(
        "Prior-year tie-out",
        passed=len(tie_out_findings) == 0,
        detail=(
            f"{len(tie_out_findings)} prior-year tie-out exception(s) found."
            if tie_out_findings else
            "Prior-year comparatives agree with the signed prior-year statements "
            "(where a prior statement was linked for comparison)."
        ),
    ))

    findings.append(_checklist_item(
        "Internal consistency",
        passed=len(consistency_findings) == 0,
        detail=(
            f"{len(consistency_findings)} internal consistency exception(s) found."
            if consistency_findings else
            "Primary statements, notes, and cross-references are internally consistent."
        ),
    ))

    findings.append(_checklist_item(
        "Spelling and grammar",
        passed=len(grammar_findings) == 0,
        detail=(
            f"{len(grammar_findings)} spelling/grammar issue(s) found."
            if grammar_findings else
            "No spelling or grammar issues identified."
        ),
        severity_if_failed="low",
    ))

    missing_sections = REQUIRED_STATEMENT_SECTIONS - set(detected_statement_types)
    findings.append(_checklist_item(
        "Required WP-514 sections present",
        passed=not missing_sections,
        detail=(
            f"Could not detect: {', '.join(sorted(missing_sections))}."
            if missing_sections else
            "Balance Sheet, Income Statement, and Cash Flow sections were all detected."
        ),
    ))

    findings.append({
        "check_type": "wp514_checklist",
        "location": "Exception resolution & sign-off",
        "severity": "low",
        "description": (
            "Exception discussion/resolution and preparer/reviewer sign-off are manual "
            "workpaper steps and are not automated by this system; confirm separately "
            "before finalizing WP-514."
        ),
    })

    return findings


def _checklist_item(name: str, passed: bool, detail: str, severity_if_failed: str = "medium") -> dict:
    return {
        "check_type": "wp514_checklist",
        "location": name,
        "severity": "info" if passed else severity_if_failed,
        "description": f"[{'PASS' if passed else 'EXCEPTION'}] {name}: {detail}",
    }
