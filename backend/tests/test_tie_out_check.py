from rules.tie_out_check import run_tie_out_check
from tests.helpers import Item


def test_detects_prior_year_mismatch_without_relying_on_the_word_prior():
    # Current statement's own "prior_year" column for Revenue.
    current_items = [
        Item("Revenue", 100, "prior_year", "P&L"),
        Item("Revenue", 128, "current_year", "P&L"),
    ]
    # The actual signed prior-year statement's figures (label has no
    # mention of "prior" at all).
    prior_statement_items = [
        Item("Revenue", 98, "current_year", "P&L"),
    ]

    findings = run_tie_out_check(current_items, prior_statement_items)

    assert len(findings) == 1
    f = findings[0]
    assert f["check_type"] == "prior_year_tie_out"
    assert f["reported_value"] == 100
    assert f["expected_value"] == 98
    assert f["difference"] == 2


def test_no_finding_when_prior_year_figures_agree():
    current_items = [Item("Revenue", 100, "prior_year", "P&L")]
    prior_statement_items = [Item("Revenue", 100, "current_year", "P&L")]

    findings = run_tie_out_check(current_items, prior_statement_items)
    assert findings == []


def test_no_prior_statement_linked_produces_no_findings():
    current_items = [Item("Revenue", 100, "prior_year", "P&L")]
    assert run_tie_out_check(current_items, []) == []


def test_only_prior_year_column_is_checked_not_current_year():
    current_items = [Item("Revenue", 100, "current_year", "P&L")]
    prior_statement_items = [Item("Revenue", 50, "current_year", "P&L")]
    # This item's year is "current_year", not "prior_year" -- it should
    # never be compared against the linked prior statement.
    assert run_tie_out_check(current_items, prior_statement_items) == []
