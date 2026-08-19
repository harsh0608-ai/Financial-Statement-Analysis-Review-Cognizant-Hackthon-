"""Generates the three synthetic financial-statement PDFs used to seed the
dummy database. Run via seed_dummy_data.py -- not meant to be run standalone,
but safe to run directly if you just want the PDFs.
"""
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "source_pdfs")
os.makedirs(OUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()


def _table_page(elements, title, rows, note=None):
    elements.append(Paragraph(title, styles["Heading1"]))
    if note:
        elements.append(Paragraph(note, styles["Normal"]))
    elements.append(Spacer(1, 12))
    data = [["Line Item", "Current Year", "Prior Year"]] + rows
    t = Table(data, colWidths=[220, 120, 120])
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ]))
    elements.append(t)
    elements.append(PageBreak())


def build_pdf(path, doc_title, sections, intro_text=None):
    doc = SimpleDocTemplate(path, pagesize=letter)
    elements = [Paragraph(doc_title, styles["Title"]), Spacer(1, 12)]
    if intro_text:
        elements.append(Paragraph(intro_text, styles["Normal"]))
        elements.append(Spacer(1, 12))
    for title, rows, note in sections:
        _table_page(elements, title, rows, note)
    doc.build(elements)


# ---------------------------------------------------------------------------
# 1. Signed prior-year statement (FY2025) -- used as the tie-out baseline.
#    Its "current_year" column is what FY2026 filings should tie back to.
# ---------------------------------------------------------------------------
PRIOR_PATH = os.path.join(OUT_DIR, "signed_prior_year_FY2025.pdf")
build_pdf(
    PRIOR_PATH,
    "Signed Financial Statements - FY2025 (Prior Year Baseline)",
    [
        ("Income Statement", [
            ["Product Revenue", "60", "55"],
            ["Service Revenue", "40", "35"],
            ["Total Revenue", "100", "90"],
            ["Salaries", "25", "22"],
            ["Rent", "10", "10"],
            ["Total Expenses", "35", "32"],
            ["Net Income", "65", "58"],
        ], None),
        ("Balance Sheet", [
            ["Cash and Cash Equivalents", "50", "40"],
            ["Accounts Receivable", "50", "45"],
            ["Inventory", "30", "28"],
            ["Total Assets", "130", "113"],
            ["Total Liabilities", "60", "55"],
            ["Total Debt", "40", "35"],
            ["Total Equity", "70", "58"],
        ], None),
        ("Cash Flow Statement", [
            ["Beginning Cash", "30", "25"],
            ["Net Increase", "20", "15"],
            ["Ending Cash", "50", "40"],
        ], None),
        ("Notes to Accounts", [
            ["Revenue", "100", "90"],
        ], None),
    ],
)

# ---------------------------------------------------------------------------
# 2. Clean current-year statement (FY2026) -- internally consistent and ties
#    out cleanly to the FY2025 baseline above. Revenue growth (100 -> 128,
#    +28%) intentionally mirrors the WP-514 mentor material's own worked
#    example, so it still produces a genuine (non-error) analytical finding.
# ---------------------------------------------------------------------------
CLEAN_PATH = os.path.join(OUT_DIR, "current_year_clean_FY2026.pdf")
build_pdf(
    CLEAN_PATH,
    "Financial Statements - FY2026 (Clean)",
    [
        ("Income Statement", [
            ["Product Revenue", "80", "60"],
            ["Service Revenue", "48", "40"],
            ["Total Revenue", "128", "100"],
            ["Salaries", "30", "25"],
            ["Rent", "10", "10"],
            ["Depreciation", "5", ""],
            ["Total Expenses", "45", "35"],
            ["Net Income", "83", "65"],
        ], None),
        ("Balance Sheet", [
            ["Cash and Cash Equivalents", "70", "50"],
            ["Accounts Receivable", "60", "50"],
            ["Inventory", "35", "30"],
            ["Total Assets", "165", "130"],
            ["Total Liabilities", "65", "60"],
            ["Total Debt", "50", "40"],
            ["Total Equity", "100", "70"],
        ], None),
        ("Cash Flow Statement", [
            ["Beginning Cash", "50", "30"],
            ["Net Increase", "20", "20"],
            ["Ending Cash", "70", "50"],
        ], None),
        ("Notes to Accounts", [
            ["Revenue", "128", "100"],
        ], None),
    ],
)

# ---------------------------------------------------------------------------
# 3. Current-year statement WITH ERRORS (FY2026) -- same shape as the clean
#    filing, but deliberately broken in several independent, realistic ways:
#      - Revenue Note (125) vs Income Statement Revenue (128)   -> consistency
#      - Prior-year Revenue (98, self-consistent) vs signed 100 -> tie-out
#      - Reported Total Assets (170) vs actual sum (165)         -> math
#      - Cash Flow Ending Cash (65) vs Balance Sheet Cash (70)   -> consistency
#      - A grammar/spelling-riddled introductory paragraph       -> grammar
# ---------------------------------------------------------------------------
BROKEN_PATH = os.path.join(OUT_DIR, "current_year_with_errors_FY2026.pdf")
build_pdf(
    BROKEN_PATH,
    "Financial Statements - FY2026 (Contains Errors)",
    [
        ("Income Statement", [
            ["Product Revenue", "80", "60"],
            ["Service Revenue", "48", "38"],
            ["Total Revenue", "128", "98"],
            ["Salaries", "30", "25"],
            ["Rent", "10", "10"],
            ["Depreciation", "5", ""],
            ["Total Expenses", "45", "35"],
            ["Net Income", "83", "63"],
        ], None),
        ("Balance Sheet", [
            ["Cash and Cash Equivalents", "70", "50"],
            ["Accounts Receivable", "60", "50"],
            ["Inventory", "35", "30"],
            ["Total Assets", "170", "130"],
            ["Total Liabilities", "65", "60"],
            ["Total Debt", "50", "40"],
            ["Total Equity", "100", "70"],
        ], None),
        ("Cash Flow Statement", [
            ["Beginning Cash", "50", "30"],
            ["Net Increase", "15", "20"],
            ["Ending Cash", "65", "50"],
        ], None),
        ("Notes to Accounts", [
            ["Revenue", "125", "98"],
        ], None),
    ],
    intro_text=(
        "This statement have been prepared in accordance with applicable "
        "accounting standereds and represent managements view of the "
        "compnay's financial position as at the reporting date."
    ),
)

if __name__ == "__main__":
    print("Generated:")
    print(" ", PRIOR_PATH)
    print(" ", CLEAN_PATH)
    print(" ", BROKEN_PATH)
