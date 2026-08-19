# Dataset expansion (60 companies, 120 statements)

This extends `dummy_finstatement.db` beyond the original 5 seed statements
with **60 synthetic companies** (120 statements: a signed FY2025 baseline +
an FY2026 current-year filing per company), run through the **real**
extraction → normalization → rule-engine pipeline — same principle as the
original `seed_dummy_data.py`, just at scale. Nothing here is hand-typed;
every finding in the database was actually produced by your `rules/` code.

Statement IDs 1–5 (the original demo) are untouched. Companies start at
statement ID 6.

## Files

| File | What it is |
|---|---|
| `dummy_data/generate_dataset.py` | Financial model + PDF builder. Produces the 120 source PDFs into `dummy_data/source_pdfs/dataset/`. |
| `dummy_data/expand_dataset.py` | Runs every generated PDF through the real pipeline and appends the results to `dummy_finstatement.db`. Also writes `companies_dataset_summary.csv`. |
| `dummy_data/companies_dataset_summary.csv` | One row per company: name, industry, category, statement IDs, and a finding count per check_type — useful for demo prep and for answering "how did you build the dataset?" |

## Regenerating

```bash
cd backend
python3 dummy_data/generate_dataset.py   # rebuild the 120 PDFs
python3 dummy_data/expand_dataset.py     # run them through the real pipeline, append to the DB
```

`expand_dataset.py` does **not** wipe the database first (unlike
`seed_dummy_data.py`), so it's meant to be run once against a freshly-seeded
DB. Re-running it will append a second copy of all 60 companies. For a quick
smoke test, `python3 dummy_data/expand_dataset.py --limit 5` only processes
the first 5 companies.

## Categories (60 companies)

Each company is deliberately built to be clean *except* for one isolated,
intentional issue, so a given company's findings map to exactly one
check_type (plus the ratio/analytical/wp514 findings every statement
naturally gets, and a small, realistic one-item disclosure gap most
categories carry alongside their main issue — see the CSV). This makes each
company easy to explain and demo.

| Category | Count | What's deliberately wrong | check_type it trips |
|---|---|---|---|
| `clean` | 20 | Nothing — fully consistent, full disclosures | *(none — only informational findings)* |
| `mathematical_error` | 10 | Reported Total Assets doesn't match Cash+AR+Inventory (and, cascading, doesn't match Liabilities+Equity) | `mathematical_accuracy` (2 findings each) |
| `prior_year_tie_out_error` | 8 | This year's filing shows prior-year comparatives that don't match the actual signed FY2025 baseline (Service Revenue, Total Revenue, Net Income, Revenue note all cascade from one altered figure) | `prior_year_tie_out` (4 findings each) |
| `internal_consistency_error` | 6 | Either the Revenue note disagrees with the Income Statement, or Cash Flow's Ending Cash disagrees with the Balance Sheet's cash (picked randomly per company) | `internal_consistency` (1 finding each) |
| `ratio_highlight` | 6 | High leverage (debt/equity ~1.6–3.2x) and stretched receivables (AR days pushed up) — informational, not an "exception" in this rule engine, but good for showing ratio-engine range in a demo | *(none — `ratio_analysis` is always info-level)* |
| `missing_disclosure` | 6 | None of the three disclosure keywords present | `optional_disclosure_presence` (3 findings each) |
| `grammar_error` | 4 | Same typo-laden intro paragraph pattern as the original seed data (subject-verb error + 2 misspellings) | `spell_grammar` (2 findings each) |

Note: two `clean` companies (`C005`, `C031`) pick up one stray
`spell_grammar` finding each — LanguageTool flags the synthetic company name
"Agro" as an unrecognized word. That's a genuine false positive from the
real grammar tool, not a bug in the dataset, and is a realistic artifact
worth knowing about if it comes up during judging.

## A fix made along the way

The original 3-statement seed data always reported "Inventory Turnover" as
unable to compute, because the P&L template had no "Cost of Goods Sold"
line (`ratio_check.py` needs one). This dataset adds a Cost of Goods Sold
row to every company's Income Statement, so all three ratios
(Accounts Receivable Days, Inventory Turnover, Debt-to-Equity) compute
successfully — useful if your demo wants to show the full ratio engine
working end-to-end.
