from rules.ratio_check import run_ratio_check
from tests.helpers import Item


def test_accounts_receivable_days_uses_correct_formula():
    items = [
        Item("Total Revenue", 730, "current_year", "P&L"),
        Item("Accounts Receivable", 150, "current_year", "Balance Sheet"),
        Item("Accounts Receivable", 50, "prior_year", "Balance Sheet"),
    ]
    findings = run_ratio_check(items)
    ar = next(f for f in findings if f["location"] == "Accounts Receivable Days")
    # Average AR = (150 + 50) / 2 = 100; 100 / 730 * 365 = 50.0
    assert ar["reported_value"] == 50.0
    assert ar["severity"] == "info"


def test_debt_to_equity_uses_correct_formula():
    items = [
        Item("Total Debt", 180, "current_year", "Balance Sheet"),
        Item("Total Equity", 100, "current_year", "Balance Sheet"),
    ]
    findings = run_ratio_check(items)
    dte = next(f for f in findings if f["location"] == "Debt-to-Equity Ratio")
    assert dte["reported_value"] == 1.8


def test_missing_data_returns_insufficient_data_result_not_a_guess():
    items = [Item("Total Debt", 180, "current_year", "Balance Sheet")]
    findings = run_ratio_check(items)
    dte = next(f for f in findings if f["location"] == "Debt-to-Equity Ratio")
    assert dte["severity"] == "low"
    assert "Unable to compute" in dte["description"]
    assert "reported_value" not in dte
