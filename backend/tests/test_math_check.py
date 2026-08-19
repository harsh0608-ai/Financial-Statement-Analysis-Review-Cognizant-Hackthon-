from rules.math_check import run_math_check
from tests.helpers import Item


def _revenue_expense_group(revenue_ok=True, expense_ok=True, table_id=1):
    """Two component/total groups: Revenue and Expenses, plus a
    Net Income row that should equal Total Revenue - Total Expenses."""
    items = [
        Item("Product Revenue", 80, "current_year", "P&L", table_id=table_id, group_id=0),
        Item("Service Revenue", 20, "current_year", "P&L", table_id=table_id, group_id=0),
        Item(
            "Total Revenue", 100 if revenue_ok else 999, "current_year", "P&L",
            table_id=table_id, group_id=0, is_total=True,
        ),
        Item("Salaries", 30, "current_year", "P&L", table_id=table_id, group_id=1),
        Item("Rent", 10, "current_year", "P&L", table_id=table_id, group_id=1),
        Item(
            "Total Expenses", 40 if expense_ok else 999, "current_year", "P&L",
            table_id=table_id, group_id=1, is_total=True,
        ),
        Item("Net Income", 60, "current_year", "P&L", table_id=table_id, group_id=2, is_total=True),
    ]
    return items


def test_clean_statement_produces_no_false_mathematical_errors():
    findings = run_math_check(_revenue_expense_group())
    assert findings == []


def test_detects_incorrect_total_in_a_group():
    findings = run_math_check(_revenue_expense_group(revenue_ok=False))
    math_findings = [f for f in findings if "Total Revenue" in f["location"]]
    assert len(math_findings) == 1
    f = math_findings[0]
    assert f["reported_value"] == 999
    assert f["expected_value"] == 100
    assert f["difference"] == 899


def test_multiple_sections_do_not_double_count_across_groups():
    # If Salaries/Rent (Expenses group) were wrongly summed into Total
    # Revenue's expected value, Total Revenue (100) would appear to
    # mismatch an expected_sum of 80+20+30+10=140. It must not.
    findings = run_math_check(_revenue_expense_group())
    revenue_findings = [f for f in findings if f["location"].endswith("Total Revenue")]
    assert revenue_findings == []


def test_known_identity_revenue_minus_expenses_equals_net_income():
    items = _revenue_expense_group()
    items[-1].value = 999  # break Net Income vs Revenue - Expenses
    findings = run_math_check(items)
    identity_findings = [f for f in findings if f["location"].endswith("Net Income")]
    assert len(identity_findings) == 1
    assert identity_findings[0]["expected_value"] == 60


def test_assets_equals_liabilities_plus_equity_identity():
    items = [
        Item("Total Assets", 500, "current_year", "Balance Sheet", is_total=True, group_id=0),
        Item("Total Liabilities", 300, "current_year", "Balance Sheet", is_total=True, group_id=1),
        Item("Total Equity", 250, "current_year", "Balance Sheet", is_total=True, group_id=2),
    ]
    findings = run_math_check(items)
    identity_findings = [f for f in findings if f["location"].endswith("Total Assets")]
    assert len(identity_findings) == 1
    assert identity_findings[0]["reported_value"] == 500
    assert identity_findings[0]["expected_value"] == 550
