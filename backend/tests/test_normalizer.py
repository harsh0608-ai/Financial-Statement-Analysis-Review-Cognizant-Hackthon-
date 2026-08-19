from extraction.normalizer import normalize_extraction, detect_statement_type


def _raw_content(page_text, table):
    return {
        "pages_text": [{"page_number": 1, "text": page_text}],
        "pages_tables": [{"page_number": 1, "tables": [table]}],
    }


def test_detects_statement_type_from_page_text():
    assert detect_statement_type("BALANCE SHEET as at 31 March") == "Balance Sheet"
    assert detect_statement_type("Statement of Changes in Equity") == "Equity Statement"
    assert detect_statement_type("Something unrelated") == "Unknown"


def test_hierarchy_groups_components_under_their_total_and_resets_after():
    table = [
        ["Revenue", None, None],
        ["Product Revenue", "80", "60"],
        ["Service Revenue", "20", "40"],
        ["Total Revenue", "100", "100"],
        ["Expenses", None, None],
        ["Salaries", "30", "25"],
        ["Rent", "10", "10"],
        ["Total Expenses", "40", "35"],
    ]
    raw = _raw_content("Income Statement", table)
    items = normalize_extraction(raw, ["current_year", "prior_year"])

    current_items = [i for i in items if i["year"] == "current_year"]
    labels = [i["label"] for i in current_items]
    assert labels == [
        "Product Revenue", "Service Revenue", "Total Revenue",
        "Salaries", "Rent", "Total Expenses",
    ]

    revenue_group = {i["group_id"] for i in current_items if i["label"] in ("Product Revenue", "Service Revenue", "Total Revenue")}
    expense_group = {i["group_id"] for i in current_items if i["label"] in ("Salaries", "Rent", "Total Expenses")}

    assert len(revenue_group) == 1
    assert len(expense_group) == 1
    assert revenue_group != expense_group

    totals = {i["label"]: i["is_total"] for i in current_items}
    assert totals["Total Revenue"] is True
    assert totals["Product Revenue"] is False


def test_number_parsing_handles_commas_and_parentheses_for_negatives():
    table = [["Net Loss", "(1,250)", "500"]]
    raw = _raw_content("Income Statement", table)
    items = normalize_extraction(raw, ["current_year", "prior_year"])
    current = next(i for i in items if i["year"] == "current_year")
    assert current["value"] == -1250.0
