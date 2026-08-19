"""Prior-year tie-out.

Per WP-514: the prior-year figures shown *inside the current statement*
must agree with the corresponding figures in the signed prior-year
financial statements (a separate, previously-reviewed filing) -- not with
anything inside the current statement itself.

`prior_statement_items` is expected to be the line items of that
previously-reviewed statement, filtered to its `year == "current_year"`
rows (i.e. what was "current" at the time that earlier statement was
filed/signed).

Matching is done purely by normalized label + statement section -- never
by checking whether the word "prior" appears in a label.
"""


def run_tie_out_check(current_items: list, prior_statement_items: list) -> list[dict]:
    findings = []

    if not prior_statement_items:
        return findings

    prior_lookup = {}
    for i in prior_statement_items:
        if i.value is None:
            continue
        key = (i.label.strip().lower(), i.statement_type)
        prior_lookup.setdefault(key, i)

    for item in current_items:
        if item.year != "prior_year":
            continue
        if item.value is None:
            continue

        key = (item.label.strip().lower(), item.statement_type)
        prior_item = prior_lookup.get(key)
        if prior_item is None:
            continue

        difference = round(abs(item.value - prior_item.value), 2)
        if difference > 0.01:
            findings.append({
                "check_type": "prior_year_tie_out",
                "location": f"{item.statement_type} / {item.label}",
                "severity": "medium",
                "description": (
                    f"Prior-year comparative for '{item.label}' shown in the current "
                    f"statements is {item.value}, but the signed prior-year financial "
                    f"statements report {prior_item.value} for '{prior_item.label}'."
                ),
                "reported_value": item.value,
                "expected_value": prior_item.value,
                "difference": difference,
                "page_number": item.page_number,
                "evidence": [
                    {"label": prior_item.label, "value": prior_item.value, "page_number": prior_item.page_number},
                ],
            })

    return findings
