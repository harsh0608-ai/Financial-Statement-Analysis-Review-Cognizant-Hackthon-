"""Optional / exploratory check -- NOT part of the official WP-514 requirements.

This preserves the backend's previous WP-514 assumption (a hard-coded list
of "required disclosures" checked for keyword presence in the extracted
text). The mentor-provided WP-514 reference material does not specify any
such requirement, so this can no longer be presented as an official WP-514
check.

It is kept here, isolated and clearly labeled, in case it is useful as a
future/optional check -- e.g. as a starting point for a real disclosure-
completeness review -- but rules.engine tags its findings distinctly
(check_type="optional_disclosure_presence") and rules.wp514_check does not
depend on it.
"""

REQUIRED_DISCLOSURES = [
    "contingent liabilities",
    "related party transactions",
    "significant accounting policies",
]


def run_optional_disclosure_check(pages_text: list) -> list[dict]:
    findings = []
    full_text = " ".join(page["text"].lower() for page in pages_text if page["text"])

    for disclosure in REQUIRED_DISCLOSURES:
        if disclosure not in full_text:
            findings.append({
                "check_type": "optional_disclosure_presence",
                "location": "Notes to Accounts",
                "severity": "low",
                "description": (
                    f"Optional check (not part of official WP-514): disclosure keyword "
                    f"'{disclosure}' was not found in the extracted text. Verify manually "
                    f"if this disclosure is expected."
                ),
            })

    return findings
