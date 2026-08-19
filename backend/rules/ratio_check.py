"""Financial ratio / analytical checks.

Only the ratios explicitly shown in the WP-514 mentor material are
implemented, using their exact formulas:

  Accounts Receivable Days = (Average Accounts Receivable / Revenue) x 365
  Inventory Turnover        = Cost of Sales / Average Inventory
  Debt-to-Equity Ratio      = Total Debt / Total Equity

All calculations are deterministic keyword lookups against the extracted
line items -- no ML/LLM involved. "Average" figures use the current- and
prior-year balances from the same statement (there is no separate
beginning/ending balance in the extracted data); this is a documented
simplification, not a fabricated value.

If a required source value is missing or ambiguous (more than one
candidate line item matches), the check returns an explicit
insufficient-data finding rather than guessing.
"""

REVENUE_KEYWORDS = ["total revenue", "net revenue", "total income"]
COGS_KEYWORDS = ["cost of sales", "cost of goods sold", "cogs"]
AR_KEYWORDS = ["accounts receivable", "trade receivables"]
INVENTORY_KEYWORDS = ["inventory", "inventories"]
DEBT_KEYWORDS = ["total debt", "total borrowings", "total loans"]
EQUITY_KEYWORDS = [
    "total equity", "total shareholders equity", "total shareholders' equity",
    "total stockholders equity", "total stockholders' equity",
]


def run_ratio_check(line_items: list) -> list[dict]:
    findings = [
        _accounts_receivable_days(line_items),
        _inventory_turnover(line_items),
        _debt_to_equity(line_items),
    ]
    return [f for f in findings if f is not None]


def _find(items: list, keywords: list[str], year: str):
    candidates = [
        i for i in items
        if i.year == year and i.value is not None
        and any(k in i.label.lower() for k in keywords)
    ]
    return candidates[0] if len(candidates) == 1 else None


def _insufficient(check_name: str, missing: list[str]) -> dict:
    return {
        "check_type": "ratio_analysis",
        "location": check_name,
        "severity": "low",
        "description": (
            f"Unable to compute {check_name}: required source value(s) not found or "
            f"ambiguous in the extracted data ({', '.join(missing)})."
        ),
    }


def _accounts_receivable_days(items: list):
    revenue_current = _find(items, REVENUE_KEYWORDS, "current_year")
    ar_current = _find(items, AR_KEYWORDS, "current_year")
    ar_prior = _find(items, AR_KEYWORDS, "prior_year")

    missing = []
    if revenue_current is None:
        missing.append("current year revenue")
    if ar_current is None:
        missing.append("current year accounts receivable")
    if ar_prior is None:
        missing.append("prior year accounts receivable")
    if missing:
        return _insufficient("Accounts Receivable Days", missing)

    if not revenue_current.value:
        return _insufficient("Accounts Receivable Days", ["non-zero revenue"])

    average_ar = round((ar_current.value + ar_prior.value) / 2, 2)
    ar_days = round((average_ar / revenue_current.value) * 365, 2)

    return {
        "check_type": "ratio_analysis",
        "location": "Accounts Receivable Days",
        "severity": "info",
        "description": (
            f"Accounts Receivable Days = (Average Accounts Receivable / Revenue) x 365 "
            f"= {ar_days} days, based on average AR of {average_ar} and revenue of "
            f"{revenue_current.value}."
        ),
        "reported_value": ar_days,
        "page_number": revenue_current.page_number,
        "evidence": [
            {"label": ar_current.label, "value": ar_current.value, "page_number": ar_current.page_number},
            {"label": ar_prior.label, "value": ar_prior.value, "page_number": ar_prior.page_number},
            {"label": revenue_current.label, "value": revenue_current.value, "page_number": revenue_current.page_number},
        ],
    }


def _inventory_turnover(items: list):
    cogs_current = _find(items, COGS_KEYWORDS, "current_year")
    inv_current = _find(items, INVENTORY_KEYWORDS, "current_year")
    inv_prior = _find(items, INVENTORY_KEYWORDS, "prior_year")

    missing = []
    if cogs_current is None:
        missing.append("current year cost of sales")
    if inv_current is None:
        missing.append("current year inventory")
    if inv_prior is None:
        missing.append("prior year inventory")
    if missing:
        return _insufficient("Inventory Turnover", missing)

    average_inventory = round((inv_current.value + inv_prior.value) / 2, 2)
    if not average_inventory:
        return _insufficient("Inventory Turnover", ["non-zero average inventory"])

    turnover = round(cogs_current.value / average_inventory, 2)

    return {
        "check_type": "ratio_analysis",
        "location": "Inventory Turnover",
        "severity": "info",
        "description": (
            f"Inventory Turnover = Cost of Sales / Average Inventory = {turnover}x, "
            f"based on cost of sales of {cogs_current.value} and average inventory of "
            f"{average_inventory}."
        ),
        "reported_value": turnover,
        "page_number": cogs_current.page_number,
        "evidence": [
            {"label": inv_current.label, "value": inv_current.value, "page_number": inv_current.page_number},
            {"label": inv_prior.label, "value": inv_prior.value, "page_number": inv_prior.page_number},
            {"label": cogs_current.label, "value": cogs_current.value, "page_number": cogs_current.page_number},
        ],
    }


def _debt_to_equity(items: list):
    debt_current = _find(items, DEBT_KEYWORDS, "current_year")
    equity_current = _find(items, EQUITY_KEYWORDS, "current_year")

    missing = []
    if debt_current is None:
        missing.append("total debt")
    if equity_current is None:
        missing.append("total equity")
    if missing:
        return _insufficient("Debt-to-Equity Ratio", missing)

    if not equity_current.value:
        return _insufficient("Debt-to-Equity Ratio", ["non-zero total equity"])

    ratio = round(debt_current.value / equity_current.value, 2)

    return {
        "check_type": "ratio_analysis",
        "location": "Debt-to-Equity Ratio",
        "severity": "info",
        "description": (
            f"Debt-to-Equity Ratio = Total Debt / Total Equity = {ratio}, based on "
            f"total debt of {debt_current.value} and total equity of "
            f"{equity_current.value}."
        ),
        "reported_value": ratio,
        "page_number": debt_current.page_number,
        "evidence": [
            {"label": debt_current.label, "value": debt_current.value, "page_number": debt_current.page_number},
            {"label": equity_current.label, "value": equity_current.value, "page_number": equity_current.page_number},
        ],
    }
