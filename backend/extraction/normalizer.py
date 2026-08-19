import re

STATEMENT_TYPE_KEYWORDS = {
    "balance sheet": "Balance Sheet",
    "profit and loss": "P&L",
    "income statement": "P&L",
    "statement of changes in equity": "Equity Statement",
    "changes in equity": "Equity Statement",
    "cash flow": "Cash Flow",
    "notes to accounts": "Notes",
}

# Rows whose label matches one of these are treated as a "total" row that
# closes out the current group of component rows (see normalize_extraction).
TOTAL_KEYWORDS = [
    "total", "subtotal", "grand total",
    "net income", "net profit", "net loss",
]

NUMBER_PATTERN = re.compile(r"[-+]?\d[\d,]*\.?\d*")


def detect_statement_type(text: str) -> str:
    lowered = text.lower()
    for keyword, label in STATEMENT_TYPE_KEYWORDS.items():
        if keyword in lowered:
            return label
    return "Unknown"


def is_total_label(label: str) -> bool:
    lowered = label.lower()
    return any(keyword in lowered for keyword in TOTAL_KEYWORDS)


HEADER_LABEL_KEYWORDS = ["particulars", "line item", "description", "account", "item"]
HEADER_VALUE_KEYWORDS = ["year", "period", "current", "prior", "previous"]


def _looks_like_year_header_cell(cell) -> bool:
    text = (cell or "").strip().lower()
    if not text:
        return True  # blank header cell
    if any(keyword in text for keyword in HEADER_VALUE_KEYWORDS):
        return True
    # A bare 4-digit year (e.g. "2026") used as a column header.
    if re.fullmatch(r"(19|20)\d{2}", text):
        return True
    return False


def is_year_header_row(row: list) -> bool:
    """True if this looks like a table header row such as
    ["Particulars", "2026", "2025"] or ["Line Item", "Current Year",
    "Previous Year"] rather than an actual financial line item. Only
    meant to be checked against the first row of a table.
    """
    if not row or len(row) < 2:
        return False

    label = (row[0] or "").strip().lower()
    label_is_headerish = (not label) or any(k in label for k in HEADER_LABEL_KEYWORDS)

    other_cells = row[1:]
    if not other_cells:
        return False

    return label_is_headerish and all(_looks_like_year_header_cell(c) for c in other_cells)


def parse_number(token: str):
    cleaned = token.replace(",", "").strip()
    if cleaned in ("", "-", "—", "–"):
        return None
    negative = False
    if cleaned.startswith("(") and cleaned.endswith(")"):
        negative = True
        cleaned = cleaned[1:-1]
    try:
        value = float(cleaned)
    except ValueError:
        return None
    return -value if negative else value


def normalize_table_row(
    row: list,
    page_number: int,
    statement_type: str,
    year_columns: list[str],
    table_id: int,
    order_index: int,
    group_id: int,
) -> tuple[list[dict], bool]:
    """Turn one raw table row into structured line items.

    Column position (not header text) determines which year a value
    belongs to, so this does not depend on the word "prior" (or any
    other specific header text) appearing anywhere.

    Returns (items, had_any_label) — had_any_label is used by the caller
    to detect section-header / boundary rows (a label with no numeric
    value in any year column), which are not stored as line items but
    are used to start a new hierarchy group.
    """
    items = []
    if not row or len(row) < 2:
        return items, False

    label = (row[0] or "").strip()
    if not label:
        return items, False

    total_row = is_total_label(label)

    for index, year in enumerate(year_columns, start=1):
        if index >= len(row):
            continue
        raw_value = row[index]
        if raw_value is None:
            continue
        value = parse_number(str(raw_value))
        if value is None:
            continue
        items.append({
            "year": year,
            "statement_type": statement_type,
            "label": label,
            "value": value,
            "page_number": page_number,
            "table_id": table_id,
            "order_index": order_index,
            "is_total": total_row,
            "group_id": group_id,
        })

    return items, True


def normalize_extraction(raw_content: dict, year_columns: list[str]) -> list[dict]:
    """Extraction -> structured financial line items.

    Preserves, per item: current/prior-year value (via `year`), the
    statement section, the line-item label, the page number, and enough
    hierarchy information (table_id / order_index / group_id / is_total)
    for the rule engine to respect parent/child relationships instead of
    summing every number on a page into one total.

    A "group" is the run of component rows between two boundaries. A
    boundary is either a section-header row (a label with no parseable
    value in any year column, e.g. "Revenue" used as a heading) or a
    total/subtotal row, which closes the group it sits under.
    """
    structured_items = []
    table_counter = 0

    for page_text, page_tables in zip(raw_content["pages_text"], raw_content["pages_tables"]):
        statement_type = detect_statement_type(page_text["text"])
        page_number = page_text["page_number"]

        for table in page_tables["tables"]:
            table_counter += 1
            table_id = table_counter
            group_id = 0
            order_index = 0

            for position, row in enumerate(table, start=1):
                order_index += 1

                if position == 1 and is_year_header_row(row):
                    # A column-header row (e.g. "Particulars | 2026 | 2025"
                    # or "Line Item | Current Year | Previous Year") -- not
                    # an actual line item. Column position, not this text,
                    # is what determines which year each later value
                    # belongs to.
                    continue

                items, had_label = normalize_table_row(
                    row, page_number, statement_type, year_columns,
                    table_id, order_index, group_id,
                )

                if not items:
                    if had_label:
                        # Section-header row (e.g. "Revenue" as a heading
                        # with no figures of its own): start a new group.
                        group_id += 1
                    continue

                structured_items.extend(items)

                if any(item["is_total"] for item in items):
                    # This row closes the group of components above it.
                    group_id += 1

    return structured_items
