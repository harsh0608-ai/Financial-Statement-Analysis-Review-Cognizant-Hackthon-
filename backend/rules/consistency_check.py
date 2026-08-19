"""Internal consistency checks.

Two layers, both deterministic and both scoped to avoid comparing
unrelated fields just because their labels happen to look similar:

1. Exact same label reported with different values across different
   locations for the same year (e.g. copy/paste drift between a table
   and a supporting schedule on another page).

2. A small, explicit set of cross-statement identity pairs drawn directly
   from the WP-514 material (Revenue vs Revenue Note, Ending Cash vs
   Balance Sheet cash, Net Income vs Statement of Changes in Equity).
   Each pair is constrained to specific statement sections on each side,
   so it only ever compares concepts the mentor material says should tie
   -- not any two similarly-labeled rows.
"""

CROSS_STATEMENT_PAIRS = [
    (
        "Revenue (Income Statement vs Revenue Note)",
        # Deliberately specific ("total revenue"/"net revenue" only, not
        # bare "revenue") so this never ambiguously matches component
        # rows like "Product Revenue" or "Service Revenue" on the P&L.
        ["P&L"], ["total revenue", "net revenue"],
        ["Notes"], ["revenue"],
    ),
    (
        "Ending Cash (Cash Flow Statement vs Balance Sheet)",
        ["Cash Flow"], ["ending cash", "cash and cash equivalents"],
        ["Balance Sheet"], ["cash and cash equivalents", "cash"],
    ),
    (
        "Net Income (Income Statement vs Statement of Changes in Equity)",
        ["P&L"], ["net income", "net profit"],
        ["Equity Statement"], ["net income", "net profit"],
    ),
]


def run_consistency_check(line_items: list) -> list[dict]:
    findings = []
    findings.extend(_check_same_label_consistency(line_items))
    findings.extend(_check_cross_statement_pairs(line_items))
    return findings


def _check_same_label_consistency(line_items: list) -> list[dict]:
    findings = []
    label_values = {}

    for item in line_items:
        key = (item.label.strip().lower(), item.year)
        label_values.setdefault(key, []).append(item)

    for (label, year), items in label_values.items():
        if len(items) < 2:
            continue

        distinct_values = sorted({i.value for i in items if i.value is not None})
        if len(distinct_values) > 1:
            findings.append({
                "check_type": "internal_consistency",
                "location": ", ".join(f"{i.statement_type} p.{i.page_number}" for i in items),
                "severity": "high",
                "description": (
                    f"Line item '{items[0].label}' for {year} has inconsistent values "
                    f"across statements: {distinct_values}."
                ),
                "difference": round(distinct_values[-1] - distinct_values[0], 2),
                "page_number": items[0].page_number,
                "evidence": [
                    {"label": i.label, "value": i.value, "page_number": i.page_number}
                    for i in items
                ],
            })

    return findings


def _match_one(items: list, statement_types: list[str], keywords: list[str], year: str):
    candidates = [
        i for i in items
        if i.year == year and i.value is not None
        and i.statement_type in statement_types
        and any(k in i.label.lower() for k in keywords)
    ]
    return candidates[0] if len(candidates) == 1 else None


def _check_cross_statement_pairs(line_items: list) -> list[dict]:
    findings = []

    for name, left_types, left_kw, right_types, right_kw in CROSS_STATEMENT_PAIRS:
        for year in ("current_year", "prior_year"):
            left = _match_one(line_items, left_types, left_kw, year)
            right = _match_one(line_items, right_types, right_kw, year)
            if left is None or right is None:
                continue

            difference = round(abs(left.value - right.value), 2)
            if difference > 0.01:
                findings.append({
                    "check_type": "internal_consistency",
                    "location": name,
                    "severity": "high",
                    "description": (
                        f"{name}: '{left.label}' ({left.statement_type}) reports "
                        f"{left.value}, but '{right.label}' ({right.statement_type}) "
                        f"reports {right.value}."
                    ),
                    "reported_value": left.value,
                    "expected_value": right.value,
                    "difference": difference,
                    "page_number": left.page_number,
                    "evidence": [
                        {"label": right.label, "value": right.value, "page_number": right.page_number},
                    ],
                })

    return findings
