"""Generates a larger synthetic dataset of company financial-statement PDFs
(prior-year signed baseline + current-year filing, per company) in the same
table format as generate_pdfs.py, so they parse identically through the real
extraction/normalization pipeline.

This module ONLY builds PDFs + an in-memory company spec list. It does not
touch the database -- see expand_dataset.py for that.

Run standalone to just regenerate the PDFs:
    python3 dummy_data/generate_dataset.py
"""
import os
import random

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "source_pdfs", "dataset")
os.makedirs(OUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()

SEED = 42

# ---------------------------------------------------------------------------
# Categories -- each company is assigned exactly one, which determines which
# single check_type its deliberate exception (if any) will trip. Counts sum
# to 60, matching the earlier discussed target range (50-100).
# ---------------------------------------------------------------------------
CLEAN = "clean"
MATH_ERROR = "mathematical_error"
TIE_OUT_ERROR = "prior_year_tie_out_error"
CONSISTENCY_ERROR = "internal_consistency_error"
RATIO_HIGHLIGHT = "ratio_highlight"
MISSING_DISCLOSURE = "missing_disclosure"
GRAMMAR_ERROR = "grammar_error"

CATEGORY_COUNTS = [
    (CLEAN, 20),
    (MATH_ERROR, 10),
    (TIE_OUT_ERROR, 8),
    (CONSISTENCY_ERROR, 6),
    (RATIO_HIGHLIGHT, 6),
    (MISSING_DISCLOSURE, 6),
    (GRAMMAR_ERROR, 4),
]

INDUSTRIES = [
    "IT Services", "Manufacturing", "Healthcare", "Retail", "FMCG",
    "Pharmaceuticals", "Logistics", "Renewable Energy", "Banking & Finance",
    "Real Estate", "EdTech", "Agritech",
]

NAME_PREFIXES = [
    "Alpha", "Bright", "Green", "Sunrise", "Future", "Blue", "Prime",
    "Apex", "Nova", "Silver", "Horizon", "Crest", "Vertex", "Orbit",
    "Summit", "Pioneer", "Zenith", "Cascade", "Meridian", "Falcon",
    "Granite", "Ember", "Lotus", "Copper", "Ivory", "Coral", "Marigold",
    "Beacon", "Anchor", "Wren", "Solace", "Harbor", "Fern", "Onyx",
    "Ridge", "Willow", "Aster", "Basalt", "Cobalt", "Delta", "Echo",
    "Frost", "Glow", "Haven", "Indigo", "Juno", "Kite", "Lumen", "Maple",
    "Nectar", "Opal", "Pulse", "Quartz", "Rove", "Sable", "Terra",
    "Umber", "Vista", "Wisp", "Yarrow",
]
NAME_SUFFIXES = [
    "Technologies", "Manufacturing", "Healthcare", "Retail", "Foods",
    "Pharma", "Logistics", "Energy", "Finance", "Properties", "Learning",
    "Agro", "Industries", "Systems", "Solutions", "Enterprises", "Textiles",
    "Chemicals", "Motors", "Infra",
]
LEGAL_FORMS = ["Pvt Ltd", "Ltd"]

REQUIRED_DISCLOSURE_SENTENCES = {
    # Kept short and given their own line (via <br/> when combined below) so
    # pdfplumber's text extraction never wraps mid-phrase -- a wrapped phrase
    # (e.g. "related party\ntransactions") would silently fail the check's
    # plain substring match, which does not normalize embedded newlines.
    "contingent liabilities": "Contingent liabilities: disclosed above.",
    "related party transactions": "Related party transactions: disclosed in notes.",
    "significant accounting policies": "Significant accounting policies: set out in notes.",
}

CLEAN_INTRO = (
    "These financial statements have been prepared in accordance with "
    "applicable accounting standards and represent management's view of "
    "the company's financial position as at the reporting date."
)
GRAMMAR_ERROR_INTRO = (
    "This statement have been prepared in accordance with applicable "
    "accounting standereds and represent managements view of the "
    "compnay's financial position as at the reporting date."
)


def _table_page(elements, title, rows, note=None):
    elements.append(Paragraph(title, styles["Heading1"]))
    if note:
        elements.append(Paragraph(note, styles["Normal"]))
        elements.append(Spacer(1, 8))
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


def _fmt(value):
    """Format a numeric line-item value for the PDF table, or '' for a
    deliberately blank cell (e.g. Depreciation's prior-year column)."""
    if value is None:
        return ""
    return str(int(round(value)))


# ---------------------------------------------------------------------------
# Financial model
# ---------------------------------------------------------------------------
def _ratios_for_category(rng, category):
    ratios = {
        "cogs_ratio": rng.uniform(0.25, 0.35),
        "salaries_ratio": rng.uniform(0.15, 0.25),
        "rent_ratio": rng.uniform(0.05, 0.10),
        "depr_ratio": rng.uniform(0.03, 0.06),
        "cash_ratio": rng.uniform(0.35, 0.55),
        "inv_ratio": rng.uniform(0.20, 0.35),
    }
    if category == RATIO_HIGHLIGHT:
        ratios["leverage"] = rng.uniform(1.6, 3.2)
        ratios["equity_ratio"] = rng.uniform(0.30, 0.45)
        ratios["ar_ratio"] = rng.uniform(0.55, 0.80)
    else:
        ratios["leverage"] = rng.uniform(0.25, 0.9)
        ratios["equity_ratio"] = rng.uniform(0.55, 0.75)
        ratios["ar_ratio"] = rng.uniform(0.30, 0.50)
    return ratios


def _compute_year(total_revenue, ratios, include_depreciation):
    product_rev = round(total_revenue * 0.6)
    service_rev = total_revenue - product_rev

    cogs = round(total_revenue * ratios["cogs_ratio"])
    salaries = round(total_revenue * ratios["salaries_ratio"])
    rent = round(total_revenue * ratios["rent_ratio"])
    depreciation = round(total_revenue * ratios["depr_ratio"]) if include_depreciation else None

    total_expenses = salaries + rent + cogs + (depreciation or 0)
    net_income = total_revenue - total_expenses

    cash = round(total_revenue * ratios["cash_ratio"])
    ar = round(total_revenue * ratios["ar_ratio"])
    inventory = round(total_revenue * ratios["inv_ratio"])
    total_assets = cash + ar + inventory

    equity = round(total_assets * ratios["equity_ratio"])
    liabilities = total_assets - equity
    debt = min(round(equity * ratios["leverage"]), liabilities)

    return {
        "product_rev": product_rev, "service_rev": service_rev,
        "total_revenue": total_revenue,
        "cogs": cogs, "salaries": salaries, "rent": rent,
        "depreciation": depreciation, "total_expenses": total_expenses,
        "net_income": net_income,
        "cash": cash, "ar": ar, "inventory": inventory,
        "total_assets": total_assets,
        "liabilities": liabilities, "equity": equity, "debt": debt,
    }


def _cash_flow(rng, year):
    beginning_cash = round(year["cash"] * rng.uniform(0.70, 0.95))
    ending_cash = year["cash"]
    net_increase = ending_cash - beginning_cash
    return {"beginning_cash": beginning_cash, "net_increase": net_increase, "ending_cash": ending_cash}


def build_company_financials(rng, category):
    ratios = _ratios_for_category(rng, category)

    base_revenue = round(100 * rng.uniform(0.5, 4.0))
    g1 = rng.uniform(0.05, 0.15)     # FY2024 -> FY2025 (baseline's own internal growth)
    g2 = rng.uniform(0.12, 0.35)     # FY2025 -> FY2026

    revenue_2024 = base_revenue
    revenue_2025 = round(revenue_2024 * (1 + g1))
    revenue_2026 = round(revenue_2025 * (1 + g2))

    y2024 = _compute_year(revenue_2024, ratios, include_depreciation=False)
    y2025 = _compute_year(revenue_2025, ratios, include_depreciation=False)
    y2026 = _compute_year(revenue_2026, ratios, include_depreciation=True)

    cf2024 = _cash_flow(rng, y2024)
    cf2025 = _cash_flow(rng, y2025)
    cf2026 = _cash_flow(rng, y2026)

    return {
        "y2024": y2024, "y2025": y2025, "y2026": y2026,
        "cf2024": cf2024, "cf2025": cf2025, "cf2026": cf2026,
    }


# ---------------------------------------------------------------------------
# PDF section builders
# ---------------------------------------------------------------------------
def _income_statement_rows(current, prior, current_cf=None, prior_cf=None):
    rows = [
        ["Product Revenue", _fmt(current["product_rev"]), _fmt(prior["product_rev"])],
        ["Service Revenue", _fmt(current["service_rev"]), _fmt(prior["service_rev"])],
        ["Total Revenue", _fmt(current["total_revenue"]), _fmt(prior["total_revenue"])],
        ["Salaries", _fmt(current["salaries"]), _fmt(prior["salaries"])],
        ["Rent", _fmt(current["rent"]), _fmt(prior["rent"])],
    ]
    if current.get("depreciation") is not None:
        rows.append(["Depreciation", _fmt(current["depreciation"]), ""])
    rows.append(["Cost of Goods Sold", _fmt(current["cogs"]), _fmt(prior["cogs"])])
    rows.append(["Total Expenses", _fmt(current["total_expenses"]), _fmt(prior["total_expenses"])])
    rows.append(["Net Income", _fmt(current["net_income"]), _fmt(prior["net_income"])])
    return rows


def _balance_sheet_rows(current, prior):
    return [
        ["Cash and Cash Equivalents", _fmt(current["cash"]), _fmt(prior["cash"])],
        ["Accounts Receivable", _fmt(current["ar"]), _fmt(prior["ar"])],
        ["Inventory", _fmt(current["inventory"]), _fmt(prior["inventory"])],
        ["Total Assets", _fmt(current["total_assets"]), _fmt(prior["total_assets"])],
        ["Total Liabilities", _fmt(current["liabilities"]), _fmt(prior["liabilities"])],
        ["Total Debt", _fmt(current["debt"]), _fmt(prior["debt"])],
        ["Total Equity", _fmt(current["equity"]), _fmt(prior["equity"])],
    ]


def _cash_flow_rows(current_cf, prior_cf):
    return [
        ["Beginning Cash", _fmt(current_cf["beginning_cash"]), _fmt(prior_cf["beginning_cash"])],
        ["Net Increase", _fmt(current_cf["net_increase"]), _fmt(prior_cf["net_increase"])],
        ["Ending Cash", _fmt(current_cf["ending_cash"]), _fmt(prior_cf["ending_cash"])],
    ]


def _notes_rows(current_revenue, prior_revenue):
    return [["Revenue", _fmt(current_revenue), _fmt(prior_revenue)]]


def _disclosure_note_text(phrases_included):
    sentences = [REQUIRED_DISCLOSURE_SENTENCES[p] for p in phrases_included]
    return "<br/>".join(sentences) if sentences else None


def build_company_pdfs(company):
    """Writes the two PDFs (baseline + current) for one company spec dict
    and returns their filesystem paths."""
    fin = company["financials"]
    category = company["category"]
    cid = company["id"]
    name = company["name"]

    # -- Baseline (FY2025 signed) -- always internally clean. --------------
    baseline_path = os.path.join(OUT_DIR, f"{cid}_signed_prior_year_FY2025.pdf")
    build_pdf(
        baseline_path,
        f"Signed Financial Statements - FY2025 (Prior Year Baseline) - {name}",
        [
            ("Income Statement", _income_statement_rows(fin["y2025"], fin["y2024"]), None),
            ("Balance Sheet", _balance_sheet_rows(fin["y2025"], fin["y2024"]), None),
            ("Cash Flow Statement", _cash_flow_rows(fin["cf2025"], fin["cf2024"]), None),
            ("Notes to Accounts", _notes_rows(fin["y2025"]["total_revenue"], fin["y2024"]["total_revenue"]),
             _disclosure_note_text(["contingent liabilities", "related party transactions", "significant accounting policies"])),
        ],
        intro_text=CLEAN_INTRO,
    )

    # -- Current year (FY2026) filing, shaped by category. ------------------
    current = dict(fin["y2026"])
    reported_prior = dict(fin["y2025"])           # what THIS pdf reports as its prior-year column
    reported_prior_notes_revenue = fin["y2025"]["total_revenue"]
    current_cf = dict(fin["cf2026"])
    reported_prior_cf = dict(fin["cf2025"])
    notes_current_revenue = current["total_revenue"]

    intro_text = CLEAN_INTRO
    disclosure_phrases = ["contingent liabilities", "related party transactions", "significant accounting policies"]

    if category == MATH_ERROR:
        error_amount = round(current["total_assets"] * company["rng"].uniform(0.03, 0.08)) or 5
        current["total_assets"] = current["total_assets"] + error_amount
        disclosure_phrases = disclosure_phrases[:2]  # minor realistic gap alongside the main issue

    elif category == TIE_OUT_ERROR:
        delta = round(reported_prior["service_rev"] * company["rng"].uniform(0.05, 0.15)) or 2
        reported_prior["service_rev"] = reported_prior["service_rev"] - delta
        reported_prior["total_revenue"] = reported_prior["product_rev"] + reported_prior["service_rev"]
        reported_prior["net_income"] = reported_prior["total_revenue"] - reported_prior["total_expenses"]
        reported_prior_notes_revenue = reported_prior["total_revenue"]
        disclosure_phrases = disclosure_phrases[:2]

    elif category == CONSISTENCY_ERROR:
        if company["rng"].random() < 0.5:
            offset = round(current["total_revenue"] * company["rng"].uniform(0.02, 0.06)) or 3
            notes_current_revenue = current["total_revenue"] - offset
        else:
            offset = round(current_cf["ending_cash"] * company["rng"].uniform(0.03, 0.08)) or 3
            current_cf["ending_cash"] = current_cf["ending_cash"] - offset
        disclosure_phrases = disclosure_phrases[:2]

    elif category == MISSING_DISCLOSURE:
        disclosure_phrases = []

    elif category == GRAMMAR_ERROR:
        intro_text = GRAMMAR_ERROR_INTRO
        disclosure_phrases = disclosure_phrases[:2]

    elif category == RATIO_HIGHLIGHT:
        disclosure_phrases = disclosure_phrases[:2]

    elif category == CLEAN:
        disclosure_phrases = disclosure_phrases  # full set, stays clean

    current_path = os.path.join(OUT_DIR, f"{cid}_current_year_FY2026.pdf")
    build_pdf(
        current_path,
        f"Financial Statements - FY2026 - {name}",
        [
            ("Income Statement", _income_statement_rows(current, reported_prior), None),
            ("Balance Sheet", _balance_sheet_rows(current, reported_prior), None),
            ("Cash Flow Statement", _cash_flow_rows(current_cf, reported_prior_cf), None),
            ("Notes to Accounts", _notes_rows(notes_current_revenue, reported_prior_notes_revenue),
             _disclosure_note_text(disclosure_phrases)),
        ],
        intro_text=intro_text,
    )

    return baseline_path, current_path


# ---------------------------------------------------------------------------
# Company spec generation
# ---------------------------------------------------------------------------
def generate_company_specs(seed=SEED):
    rng = random.Random(seed)
    used_names = set()
    specs = []
    counter = 1

    category_list = []
    for category, count in CATEGORY_COUNTS:
        category_list.extend([category] * count)
    rng.shuffle(category_list)

    for category in category_list:
        while True:
            name = f"{rng.choice(NAME_PREFIXES)} {rng.choice(NAME_SUFFIXES)} {rng.choice(LEGAL_FORMS)}"
            if name not in used_names:
                used_names.add(name)
                break
        industry = rng.choice(INDUSTRIES)
        cid = f"C{counter:03d}"
        company_rng = random.Random(seed * 1000 + counter)
        financials = build_company_financials(company_rng, category)
        specs.append({
            "id": cid,
            "name": name,
            "industry": industry,
            "category": category,
            "financials": financials,
            "rng": company_rng,
        })
        counter += 1

    return specs


if __name__ == "__main__":
    specs = generate_company_specs()
    print(f"Generating {len(specs)} companies into {OUT_DIR} ...")
    for company in specs:
        baseline_path, current_path = build_company_pdfs(company)
    print("Done.")
    for category, count in CATEGORY_COUNTS:
        print(f"  {category}: {count}")
