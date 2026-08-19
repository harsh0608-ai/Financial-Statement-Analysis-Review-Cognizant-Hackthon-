from rules.consistency_check import run_consistency_check
from tests.helpers import Item


def test_detects_conflicting_values_for_the_same_labeled_line_item():
    items = [
        Item("Cash and Cash Equivalents", 17, "current_year", "Balance Sheet", page_number=4),
        Item("Cash and Cash Equivalents", 15, "current_year", "Cash Flow", page_number=6),
    ]
    findings = run_consistency_check(items)
    # This scenario is deliberately also caught by the "Ending Cash"
    # cross-statement pair, so assert on the same-label check specifically
    # (its location lists page references, unlike the named pair check).
    same_label = [f for f in findings if f["location"].startswith("Balance Sheet p.")]
    assert len(same_label) == 1
    assert same_label[0]["severity"] == "high"


def test_no_finding_when_same_label_values_agree():
    items = [
        Item("Cash and Cash Equivalents", 17, "current_year", "Balance Sheet"),
        Item("Cash and Cash Equivalents", 17, "current_year", "Cash Flow"),
    ]
    assert run_consistency_check(items) == []


def test_cross_statement_pair_income_statement_revenue_vs_revenue_note():
    items = [
        Item("Total Revenue", 128, "current_year", "P&L"),
        Item("Revenue", 125, "current_year", "Notes"),
    ]
    findings = run_consistency_check(items)
    pair_findings = [f for f in findings if "Revenue Note" in f["location"]]
    assert len(pair_findings) == 1
    assert pair_findings[0]["reported_value"] == 128
    assert pair_findings[0]["expected_value"] == 125


def test_does_not_compare_unrelated_similarly_labeled_fields():
    # "Revenue" appears on a Balance Sheet page (e.g. as a stray note
    # reference) and should not be compared to the Notes "Revenue" figure
    # -- the pair is scoped to P&L vs Notes only.
    items = [
        Item("Revenue", 999, "current_year", "Balance Sheet"),
        Item("Revenue", 125, "current_year", "Notes"),
    ]
    findings = run_consistency_check(items)
    pair_findings = [f for f in findings if "Revenue Note" in f["location"]]
    assert pair_findings == []
