from rules.analytical_check import run_analytical_check
from tests.helpers import Item


def test_significant_movement_breaches_configured_threshold():
    items = [
        Item("Revenue", 128, "current_year", "P&L"),
        Item("Revenue", 100, "prior_year", "P&L"),
    ]
    findings = run_analytical_check(items, threshold_percent=10)

    assert len(findings) == 1
    f = findings[0]
    assert f["current_year_value"] == 128
    assert f["prior_year_value"] == 100
    assert f["difference"] == 28
    assert f["percentage_change"] == 28.0
    assert f["threshold"] == 10


def test_movement_below_threshold_is_not_flagged():
    items = [
        Item("Rent", 102, "current_year", "P&L"),
        Item("Rent", 100, "prior_year", "P&L"),
    ]
    findings = run_analytical_check(items, threshold_percent=10)
    assert findings == []


def test_threshold_is_configurable_not_hardcoded():
    items = [
        Item("Marketing", 112, "current_year", "P&L"),
        Item("Marketing", 100, "prior_year", "P&L"),
    ]
    assert run_analytical_check(items, threshold_percent=20) == []
    assert len(run_analytical_check(items, threshold_percent=5)) == 1


def test_missing_prior_year_value_is_skipped_gracefully():
    items = [Item("Revenue", 128, "current_year", "P&L")]
    assert run_analytical_check(items, threshold_percent=10) == []
