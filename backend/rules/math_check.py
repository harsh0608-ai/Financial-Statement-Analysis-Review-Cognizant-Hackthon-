"""Mathematical accuracy checks.

Two independent, deterministic checks:

1. Component -> subtotal/total: within a single contiguous group of rows
   (as delimited by the extraction/normalization layer's table_id/group_id
   hierarchy), the non-total rows must sum to the total row that closes
   the group. Groups are scoped per table and per section, so components
   from unrelated sections are never combined and subtotals are never
   double-counted into a later, unrelated total.

2. Known financial identities: Revenue - Expenses = Net Income, and
   Assets = Liabilities + Equity. These are only checked when exactly one
   unambiguous candidate line item is found for each side; if the data is
   ambiguous or incomplete, nothing is fabricated and the check is skipped.
"""

REVENUE_TOTAL_KEYWORDS = ["total revenue", "total income", "net revenue"]
EXPENSE_TOTAL_KEYWORDS = ["total expense", "total expenses", "total cost", "total costs"]
NET_INCOME_KEYWORDS = ["net income", "net profit", "net loss"]
ASSET_TOTAL_KEYWORDS = ["total assets"]
LIABILITY_TOTAL_KEYWORDS = ["total liabilities"]
EQUITY_TOTAL_KEYWORDS = [
    "total equity", "total shareholders equity", "total shareholders' equity",
    "total stockholders equity", "total stockholders' equity",
]


def run_math_check(line_items: list) -> list[dict]:
    findings = []
    findings.extend(_check_component_subtotal_groups(line_items))
    findings.extend(_check_known_identities(line_items))
    return findings


def _check_component_subtotal_groups(line_items: list) -> list[dict]:
    findings = []
    grouped = {}

    for item in line_items:
        table_id = getattr(item, "table_id", None)
        group_id = getattr(item, "group_id", None)
        if table_id is None or group_id is None:
            # No hierarchy info available (e.g. legacy data) -- skip
            # rather than risk combining unrelated rows.
            continue
        key = (item.statement_type, item.year, table_id, group_id)
        grouped.setdefault(key, []).append(item)

    for (statement_type, year, table_id, group_id), items in grouped.items():
        totals = [i for i in items if getattr(i, "is_total", False)]
        components = [i for i in items if not getattr(i, "is_total", False)]

        if not totals or not components:
            continue

        expected_sum = round(sum(i.value for i in components if i.value is not None), 2)

        for total_item in totals:
            if total_item.value is None:
                continue
            difference = round(abs(round(total_item.value, 2) - expected_sum), 2)
            if difference > 0.01:
                findings.append({
                    "check_type": "mathematical_accuracy",
                    "location": f"{statement_type} / {year} / {total_item.label}",
                    "severity": "high",
                    "description": (
                        f"Reported '{total_item.label}' is {total_item.value}, but the sum of its "
                        f"component line items ({', '.join(c.label for c in components)}) is "
                        f"{expected_sum}."
                    ),
                    "reported_value": total_item.value,
                    "expected_value": expected_sum,
                    "difference": difference,
                    "page_number": total_item.page_number,
                    "evidence": [
                        {"label": c.label, "value": c.value, "page_number": c.page_number}
                        for c in components
                    ],
                })

    return findings


def _match_single(items: list, keywords: list[str]):
    matches = [i for i in items if i.value is not None and any(k in i.label.lower() for k in keywords)]
    return matches[0] if len(matches) == 1 else None


def _check_known_identities(line_items: list) -> list[dict]:
    findings = []
    by_year = {}
    for item in line_items:
        by_year.setdefault(item.year, []).append(item)

    for year, items in by_year.items():
        revenue_total = _match_single(items, REVENUE_TOTAL_KEYWORDS)
        expense_total = _match_single(items, EXPENSE_TOTAL_KEYWORDS)
        net_income = _match_single(items, NET_INCOME_KEYWORDS)

        if revenue_total and expense_total and net_income:
            expected = round(revenue_total.value - expense_total.value, 2)
            difference = round(abs(net_income.value - expected), 2)
            if difference > 0.01:
                findings.append({
                    "check_type": "mathematical_accuracy",
                    "location": f"{year} / {net_income.label}",
                    "severity": "high",
                    "description": (
                        f"Reported '{net_income.label}' is {net_income.value}, but "
                        f"'{revenue_total.label}' ({revenue_total.value}) minus "
                        f"'{expense_total.label}' ({expense_total.value}) is {expected}."
                    ),
                    "reported_value": net_income.value,
                    "expected_value": expected,
                    "difference": difference,
                    "page_number": net_income.page_number,
                    "evidence": [
                        {"label": revenue_total.label, "value": revenue_total.value, "page_number": revenue_total.page_number},
                        {"label": expense_total.label, "value": expense_total.value, "page_number": expense_total.page_number},
                    ],
                })

        assets = _match_single(items, ASSET_TOTAL_KEYWORDS)
        liabilities = _match_single(items, LIABILITY_TOTAL_KEYWORDS)
        equity = _match_single(items, EQUITY_TOTAL_KEYWORDS)

        if assets and liabilities and equity:
            expected = round(liabilities.value + equity.value, 2)
            difference = round(abs(assets.value - expected), 2)
            if difference > 0.01:
                findings.append({
                    "check_type": "mathematical_accuracy",
                    "location": f"{year} / {assets.label}",
                    "severity": "high",
                    "description": (
                        f"Reported '{assets.label}' is {assets.value}, but "
                        f"'{liabilities.label}' ({liabilities.value}) plus "
                        f"'{equity.label}' ({equity.value}) is {expected}."
                    ),
                    "reported_value": assets.value,
                    "expected_value": expected,
                    "difference": difference,
                    "page_number": assets.page_number,
                    "evidence": [
                        {"label": liabilities.label, "value": liabilities.value, "page_number": liabilities.page_number},
                        {"label": equity.label, "value": equity.value, "page_number": equity.page_number},
                    ],
                })

    return findings
