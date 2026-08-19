"""Planning / analytical review.

Current-year vs prior-year movement for every line item, per the WP-514
material's worked example (Revenue: 100M -> 128M = +28M / +28%). Movements
whose absolute percentage change meets or exceeds a configurable threshold
are flagged for investigation.

The threshold is never hard-coded into the check itself -- it is read from
config.ANALYTICAL_THRESHOLD_PERCENT by default, and can be overridden per
call.
"""

from config import ANALYTICAL_THRESHOLD_PERCENT


def run_analytical_check(line_items: list, threshold_percent: float = None) -> list[dict]:
    findings = []
    threshold = ANALYTICAL_THRESHOLD_PERCENT if threshold_percent is None else threshold_percent

    current_lookup = {}
    prior_lookup = {}

    for item in line_items:
        if item.value is None:
            continue
        key = (item.label.strip().lower(), item.statement_type)
        if item.year == "current_year":
            current_lookup.setdefault(key, item)
        elif item.year == "prior_year":
            prior_lookup.setdefault(key, item)

    for key, current_item in current_lookup.items():
        prior_item = prior_lookup.get(key)
        if prior_item is None or not prior_item.value:
            continue

        absolute_change = round(current_item.value - prior_item.value, 2)
        percentage_change = round((absolute_change / prior_item.value) * 100, 2)

        if abs(percentage_change) < threshold:
            continue

        severity = "high" if abs(percentage_change) >= threshold * 2 else "medium"

        findings.append({
            "check_type": "analytical_review",
            "location": f"{current_item.statement_type} / {current_item.label}",
            "severity": severity,
            "description": (
                f"'{current_item.label}' moved from {prior_item.value} to "
                f"{current_item.value} ({percentage_change:+.2f}%), exceeding the "
                f"{threshold}% planning/analytical threshold."
            ),
            "current_year_value": current_item.value,
            "prior_year_value": prior_item.value,
            "difference": absolute_change,
            "percentage_change": percentage_change,
            "threshold": threshold,
            "page_number": current_item.page_number,
        })

    return findings
