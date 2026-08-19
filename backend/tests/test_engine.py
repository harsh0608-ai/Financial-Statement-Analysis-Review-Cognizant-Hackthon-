import rules.engine as engine
from rules.engine import run_all_checks
from tests.helpers import Item


def _clean_statement():
    return [
        Item("Product Revenue", 80, "current_year", "P&L", table_id=1, group_id=0),
        Item("Service Revenue", 20, "current_year", "P&L", table_id=1, group_id=0),
        Item("Total Revenue", 100, "current_year", "P&L", table_id=1, group_id=0, is_total=True),
        Item("Product Revenue", 60, "prior_year", "P&L", table_id=1, group_id=0),
        Item("Service Revenue", 40, "prior_year", "P&L", table_id=1, group_id=0),
        Item("Total Revenue", 100, "prior_year", "P&L", table_id=1, group_id=0, is_total=True),
    ]


def test_combined_errors_produce_multiple_independent_findings(monkeypatch):
    # Silence spell/grammar so this test is hermetic (no LanguageTool/Java
    # dependency) and isolate the scenario to math + tie-out + analytical.
    monkeypatch.setattr(engine, "run_spell_grammar_check", lambda pages_text: [])

    current_items = [
        Item("Product Revenue", 80, "current_year", "P&L", table_id=1, group_id=0),
        Item("Service Revenue", 20, "current_year", "P&L", table_id=1, group_id=0),
        # Wrong total -> mathematical_accuracy finding
        Item("Total Revenue", 999, "current_year", "P&L", table_id=1, group_id=0, is_total=True),
        # Large movement vs prior_year column -> analytical_review finding
        Item("Total Revenue", 100, "prior_year", "P&L", table_id=1, group_id=0, is_total=True),
    ]
    prior_statement_items = [Item("Total Revenue", 50, "current_year", "P&L")]

    findings = run_all_checks(
        current_items, pages_text=[{"page_number": 1, "text": ""}],
        prior_statement_items=prior_statement_items,
        analytical_threshold_percent=10,
    )

    check_types = {f["check_type"] for f in findings}
    assert "mathematical_accuracy" in check_types
    assert "prior_year_tie_out" in check_types
    assert "analytical_review" in check_types
    assert "wp514_checklist" in check_types


def test_grammar_check_failure_does_not_block_other_checks(monkeypatch):
    def _boom(pages_text):
        raise RuntimeError("LanguageTool unavailable")

    monkeypatch.setattr(engine, "run_spell_grammar_check", _boom)

    current_items = [
        Item("Product Revenue", 80, "current_year", "P&L", table_id=1, group_id=0),
        Item("Service Revenue", 20, "current_year", "P&L", table_id=1, group_id=0),
        Item("Total Revenue", 999, "current_year", "P&L", table_id=1, group_id=0, is_total=True),
    ]

    findings = run_all_checks(current_items, pages_text=[{"page_number": 1, "text": "irrelevant"}])

    check_types = {f["check_type"] for f in findings}
    assert "mathematical_accuracy" in check_types
    assert "spell_grammar" not in check_types  # the failed check simply contributes nothing


def test_missing_ratio_data_yields_graceful_insufficient_data_result(monkeypatch):
    monkeypatch.setattr(engine, "run_spell_grammar_check", lambda pages_text: [])

    items = [Item("Total Debt", 180, "current_year", "Balance Sheet")]
    findings = run_all_checks(items, pages_text=[{"page_number": 1, "text": ""}])

    ratio_findings = [f for f in findings if f["check_type"] == "ratio_analysis"]
    assert ratio_findings, "expected insufficient-data ratio findings, got none"
    assert all(f["severity"] == "low" for f in ratio_findings)


def test_a_single_check_raising_does_not_crash_the_whole_engine(monkeypatch):
    def _boom(line_items):
        raise RuntimeError("boom")

    monkeypatch.setattr(engine, "run_math_check", _boom)

    findings = run_all_checks(_clean_statement(), pages_text=[{"page_number": 1, "text": ""}])
    # Should not raise, and other checks should still have run.
    check_types = {f["check_type"] for f in findings}
    assert "mathematical_accuracy" not in check_types
    assert "wp514_checklist" in check_types
