"""
Hand-verified WP-514 knowledge base content.

IMPORTANT — VERIFICATION METHODOLOGY:
Every piece of text below was manually read from the 4 mentor-provided
WP-514 images and verified against the original photographs.  OCR was NOT
blindly trusted — all formulas, dollar amounts, percentages, and technical
terms were cross-checked against the source images.

Where the image was unclear, the content was marked [UNCLEAR IN SOURCE] and
omitted rather than fabricated.

Source: 4 WhatsApp images from industrial mentor, dated 2026-08-17.
Document title: "Understanding the WP-514 Statement"
Subtitle: "Plain-language explanation, expected activities, evidence,
           and review checklist"

Each entry is a dict with:
  - section_id:  Unique section identifier
  - title:       Section heading
  - content:     Full verified text
  - topic:       Classification for metadata filtering
  - page:        Source image number (1-4)
  - source:      Always "WP514_mentor_reference"
"""

WP514_SECTIONS: list[dict] = [
    # ──────────────────────────────────────────────────────────────────
    # IMAGE 1 (LEFT SIDE) — Pages 1-2 of the document
    # ──────────────────────────────────────────────────────────────────
    {
        "section_id": "wp514_original_statement",
        "title": "Original WP-514 Statement",
        "content": (
            "Original statement: \"Generate, populate, and review financial statement "
            "planning analytics, perform financial statement review (e.g., mathematical "
            "accuracy, prior year tie out, internal consistency, spelling and grammar, "
            "etc.) and WP-514 from financial statements.\""
        ),
        "topic": "wp514_general",
        "page": 1,
        "source": "WP514_mentor_reference",
    },
    {
        "section_id": "wp514_plain_language",
        "title": "Plain-Language Meaning",
        "content": (
            "In simple terms, the statement means: use the draft financial statements "
            "as the source to prepare the required planning analytics and the WP-514 "
            "workpaper, then review both the financial statements and WP-514 for "
            "numerical accuracy, consistency, completeness, and presentation quality. "
            "Any differences or exceptions should be investigated, documented, "
            "corrected, or clearly carried forward for review.\n\n"
            "Important assumption: \"WP-514\" appears to be an organization- or "
            "engagement-specific financial statement workpaper/template. Its exact "
            "fields, sign-offs, and purpose should be interpreted using the applicable "
            "audit methodology, template instructions, and reviewer guidance."
        ),
        "topic": "wp514_general",
        "page": 1,
        "source": "WP514_mentor_reference",
    },
    {
        "section_id": "wp514_requirements_table",
        "title": "Breakdown of Each Requirement",
        "content": (
            "Activity: Generate planning analytics\n"
            "What it involves: Create analytical comparisons from the financial "
            "statements, such as current year versus prior year movements, key ratios, "
            "unusual fluctuations, and balances requiring audit attention.\n"
            "Expected evidence/output: A completed planning analytics schedule with "
            "explanations for significant movements.\n\n"
            "Activity: Populate WP-514\n"
            "What it involves: Transfer or link the required financial statement data "
            "into the WP-514 template. Complete all mandatory sections, references, "
            "conclusions, and preparer details.\n"
            "Expected evidence/output: A fully completed WP-514 that agrees to the "
            "latest financial statements.\n\n"
            "Activity: Review planning analytics\n"
            "What it involves: Check whether the analysis is complete, uses the correct "
            "periods and data, applies appropriate thresholds, and identifies unusual "
            "or unexpected relationships.\n"
            "Expected evidence/output: Reviewed analytics with investigated variances "
            "and documented conclusions.\n\n"
            "Activity: Mathematical accuracy\n"
            "What it involves: Recalculate totals, subtotals, cross-casts, earnings, "
            "cash-flow movements, note totals, and other arithmetic relationships.\n"
            "Expected evidence/output: Evidence that formulas, additions, and "
            "cross-references are accurate.\n\n"
            "Activity: Prior-year tie-out\n"
            "What it involves: Compare prior-year figures shown in the current financial "
            "statements with the prior-year signed or final financial statements.\n"
            "Expected evidence/output: Prior-year comparative amounts agree, or "
            "differences are explained and documented.\n\n"
            "Activity: Internal consistency\n"
            "What it involves: Confirm that the same figure and description are "
            "consistent across the primary statements, notes, accounting policies, "
            "and related disclosures.\n"
            "Expected evidence/output: No unexplained contradictions among statements "
            "and notes.\n\n"
            "Activity: Spelling and grammar\n"
            "What it involves: Review wording, headings, dates, entity names, currency "
            "labels, terminology, punctuation, and formatting.\n"
            "Expected evidence/output: Financial statements are professionally "
            "presented and free of obvious drafting errors.\n\n"
            "Activity: Complete WP-514 review\n"
            "What it involves: Ensure the workpaper reflects the final financial "
            "statements, exceptions are resolved, references are clear.\n"
            "Expected evidence/output: A review-ready workpaper with a clear "
            "conclusion and audit trail."
        ),
        "topic": "wp514_general",
        "page": 1,
        "source": "WP514_mentor_reference",
    },

    # ──────────────────────────────────────────────────────────────────
    # IMAGE 1 (RIGHT SIDE)
    # ──────────────────────────────────────────────────────────────────
    {
        "section_id": "wp514_workflow",
        "title": "Practical End-to-End Workflow",
        "content": (
            "Step 1. Obtain the source documents: Use the latest draft financial "
            "statements, prior-year signed financial statements, trial balance or lead "
            "schedules, disclosure checklists, and the approved WP-514 template.\n\n"
            "Step 2. Prepare the analytics: Calculate year-on-year movements, "
            "percentages, ratios, and other required planning measures. Flag "
            "significant or unexpected changes.\n\n"
            "Step 3. Populate WP-514: Enter or link the required amounts, descriptions, "
            "references, thresholds, explanations, and conclusions. Clearly identify "
            "the source of each amount.\n\n"
            "Step 4. Perform the financial statement review: Check arithmetic, "
            "prior-year comparatives, note-to-statement agreement, consistency of "
            "terminology, dates, currencies, cross-references, spelling, and grammar.\n\n"
            "Step 5. Resolve exceptions: Discuss differences with the appropriate team "
            "member, update the financial statements or workpaper, and retain "
            "explanations and supporting evidence.\n\n"
            "Step 6. Finalize and sign off: Confirm WP-514 agrees to the final "
            "financial statements, all review points are cleared, the conclusion is "
            "supported, and preparer/reviewer sign-offs are completed."
        ),
        "topic": "wp514_general",
        "page": 1,
        "source": "WP514_mentor_reference",
    },
    {
        "section_id": "wp514_reviewer_example",
        "title": "Example of How a Reviewer May Apply the Statement",
        "content": (
            "Assume revenue in the draft financial statements increased from "
            "$100 million in the prior year to $128 million in the current year. "
            "The preparer would:\n\n"
            "- Calculate the increase of $28 million and 28%, and determine whether "
            "it exceeds the planning or investigation threshold.\n"
            "- Document the business explanation and corroborating source, such as "
            "volume growth, pricing changes, an acquisition, or new contracts.\n"
            "- Confirm the prior-year amount of $100 million agrees to the signed "
            "prior-year financial statements.\n"
            "- Check that $128 million agrees across the income statement, revenue "
            "note, segment disclosure, and any related narrative.\n"
            "- Ensure the amount, explanation, references, and conclusion are "
            "accurately reflected in WP-514.\n"
            "- Correct or document any difference before submitting the workpaper "
            "for review."
        ),
        "topic": "planning_analytics",
        "page": 1,
        "source": "WP514_mentor_reference",
    },
    {
        "section_id": "wp514_review_checklist",
        "title": "Suggested WP-514 Review Checklist",
        "content": (
            "Checklist items:\n"
            "1. Correct entity, reporting period, currency, and version of the "
            "financial statements used.\n"
            "2. All required WP-514 sections completed; no unexplained blanks or "
            "stale prior-year content.\n"
            "3. Current-year and prior-year amounts agree to the appropriate source "
            "documents.\n"
            "4. Planning analytics are mathematically accurate and significant "
            "movements are explained.\n"
            "5. Primary statements, notes, disclosures, and cross-references are "
            "internally consistent.\n"
            "6. Totals, subtotals, cross-casts, and note references have been "
            "recalculated or checked.\n"
            "7. Prior-year comparatives agree to the final signed prior-year "
            "financial statements.\n"
            "8. Spelling, grammar, headings, dates, names, units, and formatting "
            "are consistent.\n"
            "9. Exceptions and review comments are resolved or clearly documented "
            "with ownership.\n"
            "10. Conclusion is clear, evidence-based, and aligned with the work "
            "performed.\n"
            "11. Preparer and reviewer names, dates, sign-offs, and version control "
            "are complete."
        ),
        "topic": "wp514_general",
        "page": 2,
        "source": "WP514_mentor_reference",
    },

    # ──────────────────────────────────────────────────────────────────
    # IMAGE 2 (LEFT SIDE)
    # ──────────────────────────────────────────────────────────────────
    {
        "section_id": "wp514_clearer_rewording",
        "title": "Clearer Rewording of the Original Statement",
        "content": (
            "\"Using the draft financial statements, prepare and populate the required "
            "planning analytics and WP-514 workpaper. Review the financial statements "
            "and WP-514 for arithmetic accuracy, agreement with prior-year signed "
            "statements, internal consistency across statements and notes, completeness, "
            "spelling, grammar, and presentation. Investigate and document any "
            "exceptions, update the workpaper for resolved items, and complete the "
            "required preparer and reviewer sign-offs.\""
        ),
        "topic": "wp514_general",
        "page": 2,
        "source": "WP514_mentor_reference",
    },
    {
        "section_id": "wp514_key_takeaway",
        "title": "Key Takeaway",
        "content": (
            "The task is not only data entry. It combines preparation, analytical "
            "review, detailed financial statement checking, exception resolution, "
            "documentation, and sign-off. WP-514 should provide a traceable record "
            "showing what was checked, what issues were identified, how they were "
            "resolved, and the final conclusion."
        ),
        "topic": "wp514_general",
        "page": 2,
        "source": "WP514_mentor_reference",
    },
    {
        "section_id": "example_revenue_analytics",
        "title": "Example 1: Revenue Analytics",
        "content": (
            "Revenue Analytics — Planning / Analytical Review Example\n\n"
            "Current Year: $128M\n"
            "Prior Year: $100M\n"
            "Increase: $28M\n"
            "Percentage Increase: 28%\n\n"
            "Review steps:\n"
            "- Compare increase against planning threshold.\n"
            "- Obtain management explanation for the increase.\n"
            "- Validate consistency with revenue disclosures and business performance "
            "reports.\n\n"
            "Review Conclusion: Revenue growth is reasonable and supported by business "
            "expansion."
        ),
        "topic": "planning_analytics",
        "page": 2,
        "source": "WP514_mentor_reference",
    },

    # ──────────────────────────────────────────────────────────────────
    # IMAGE 2 (RIGHT SIDE)
    # ──────────────────────────────────────────────────────────────────
    {
        "section_id": "example_gross_margin",
        "title": "Example 2: Gross Profit Margin Analysis",
        "content": (
            "Gross Profit Margin Analysis\n\n"
            "Particulars     | Current Year | Prior Year\n"
            "Revenue         | $128M        | $100M\n"
            "Cost of Sales   | $90M         | $75M\n"
            "Gross Profit    | $38M         | $25M\n"
            "Gross Margin %  | 29.7%        | 25.0%\n\n"
            "Analytics:\n"
            "- Gross margin increased from 25.0% to 29.7%.\n"
            "- Investigate whether pricing, product mix, or procurement efficiencies "
            "caused the improvement.\n\n"
            "Potential Risk: Unexpected improvement may indicate cutoff issues, "
            "inventory valuation errors, or incorrect expense classification."
        ),
        "topic": "planning_analytics",
        "page": 2,
        "source": "WP514_mentor_reference",
    },
    {
        "section_id": "example_opex_analysis",
        "title": "Example 3: Operating Expense Analysis",
        "content": (
            "Operating Expense Analysis\n\n"
            "Expense Category | Current Year | Prior Year | Variance\n"
            "Payroll          | $25M         | $20M       | 25%\n"
            "Marketing        | $10M         | $7M        | 43%\n"
            "IT Costs         | $8M          | $6M        | 33%\n\n"
            "Analytics:\n"
            "- Identify significant increases.\n"
            "- Compare with budget and business growth.\n"
            "- Obtain explanations from management for unusual movements."
        ),
        "topic": "planning_analytics",
        "page": 2,
        "source": "WP514_mentor_reference",
    },
    {
        "section_id": "example_ar_days",
        "title": "Example 4: Accounts Receivable Days",
        "content": (
            "Accounts Receivable Days — Ratio Analysis\n\n"
            "Formula:\n"
            "Accounts Receivable Days = (Average Accounts Receivable / Revenue) x 365\n\n"
            "Year          | AR Days\n"
            "Current Year  | 75\n"
            "Prior Year    | 52\n\n"
            "Analytics:\n"
            "- Increase of 23 days.\n"
            "- Assess possible collection issues.\n"
            "- Review aged receivable balances.\n"
            "- Identify overdue customer accounts.\n\n"
            "Potential Audit Focus: Recoverability and allowance for doubtful accounts."
        ),
        "topic": "ratio_analysis",
        "page": 2,
        "source": "WP514_mentor_reference",
    },

    # ──────────────────────────────────────────────────────────────────
    # IMAGE 3 (LEFT SIDE)
    # ──────────────────────────────────────────────────────────────────
    {
        "section_id": "example_inventory_turnover",
        "title": "Example 5: Inventory Turnover",
        "content": (
            "Inventory Turnover — Ratio Analysis\n\n"
            "Formula:\n"
            "Inventory Turnover = Cost of Sales / Average Inventory\n\n"
            "Year          | Turnover\n"
            "Current Year  | 4.2x\n"
            "Prior Year    | 6.5x\n\n"
            "Analytics:\n"
            "- Declining turnover may indicate obsolete inventory.\n"
            "- Review aging reports and slow-moving stock."
        ),
        "topic": "ratio_analysis",
        "page": 3,
        "source": "WP514_mentor_reference",
    },
    {
        "section_id": "example_cash_flow_consistency",
        "title": "Example 6: Cash Flow Consistency Check",
        "content": (
            "Cash Flow Consistency Check — Internal Consistency\n\n"
            "Review Steps:\n"
            "- Verify ending cash in Cash Flow Statement agrees with Balance Sheet.\n"
            "- Confirm major investing and financing activities are properly disclosed.\n"
            "- Recalculate cash movement reconciliation.\n\n"
            "Example:\n"
            "Beginning Cash: $12M\n"
            "Net Increase: $5M\n"
            "Ending Cash: $17M\n\n"
            "Ensure ending cash of $17M agrees across all statements."
        ),
        "topic": "cash_flow_consistency",
        "page": 3,
        "source": "WP514_mentor_reference",
    },

    # ──────────────────────────────────────────────────────────────────
    # IMAGE 3 (RIGHT SIDE)
    # ──────────────────────────────────────────────────────────────────
    {
        "section_id": "example_debt_ratio",
        "title": "Example 7: Debt Ratio Analysis",
        "content": (
            "Debt Ratio Analysis — Ratio Analysis\n\n"
            "Formula:\n"
            "Debt to Equity Ratio = Total Debt / Total Equity\n\n"
            "Year          | Ratio\n"
            "Current Year  | 1.8\n"
            "Prior Year    | 1.2\n\n"
            "Analytics:\n"
            "- Investigate significant increase.\n"
            "- Assess new borrowings.\n"
            "- Review compliance with loan covenants."
        ),
        "topic": "ratio_analysis",
        "page": 3,
        "source": "WP514_mentor_reference",
    },
    {
        "section_id": "example_prior_year_tieout",
        "title": "Example 8: Prior Year Tie-Out",
        "content": (
            "Prior Year Tie-Out\n\n"
            "Review Performed:\n"
            "- Prior-year revenue in 2026 statements = $100M.\n"
            "- Compare to signed 2025 financial statements.\n"
            "- Confirm exact agreement.\n\n"
            "Exception Example:\n"
            "- Current statements show $100M.\n"
            "- Prior signed statements show $98M.\n\n"
            "Action Required:\n"
            "- Identify whether restatement occurred.\n"
            "- Verify disclosure requirements.\n"
            "- Update WP-514 documentation."
        ),
        "topic": "prior_year_consistency",
        "page": 3,
        "source": "WP514_mentor_reference",
    },
    {
        "section_id": "example_internal_consistency",
        "title": "Example 9: Internal Consistency Review",
        "content": (
            "Internal Consistency Review\n\n"
            "Check that:\n"
            "- Revenue in Income Statement agrees with Revenue Note.\n"
            "- Net Income agrees with Statement of Changes in Equity.\n"
            "- Ending Cash agrees between Balance Sheet and Cash Flow Statement.\n"
            "- Earnings Per Share agrees with supporting calculations.\n\n"
            "Example Finding:\n"
            "Income Statement Revenue = $128M\n"
            "Revenue Note = $125M\n\n"
            "Result: Exception to be investigated and corrected."
        ),
        "topic": "internal_consistency",
        "page": 3,
        "source": "WP514_mentor_reference",
    },

    # ──────────────────────────────────────────────────────────────────
    # Extracted from the requirements table and checklist — dedicated
    # sections for check_types that aren't covered by a standalone example
    # ──────────────────────────────────────────────────────────────────
    {
        "section_id": "mathematical_accuracy_guidance",
        "title": "Mathematical Accuracy — WP-514 Guidance",
        "content": (
            "Mathematical Accuracy Review\n\n"
            "What it involves: Recalculate totals, subtotals, cross-casts, earnings, "
            "cash-flow movements, note totals, and other arithmetic relationships.\n\n"
            "Expected evidence/output: Evidence that formulas, additions, and "
            "cross-references are accurate.\n\n"
            "Checklist item: Totals, subtotals, cross-casts, and note references "
            "have been recalculated or checked.\n\n"
            "Checklist item: Planning analytics are mathematically accurate and "
            "significant movements are explained.\n\n"
            "In the financial statement review step, check arithmetic including "
            "recalculation of totals, subtotals, and cross-casts to ensure formulas, "
            "additions, and cross-references are accurate."
        ),
        "topic": "mathematical_accuracy",
        "page": 1,
        "source": "WP514_mentor_reference",
    },
    {
        "section_id": "spell_grammar_guidance",
        "title": "Spelling and Grammar — WP-514 Guidance",
        "content": (
            "Spelling and Grammar Review\n\n"
            "What it involves: Review wording, headings, dates, entity names, "
            "currency labels, terminology, punctuation, and formatting.\n\n"
            "Expected evidence/output: Financial statements are professionally "
            "presented and free of obvious drafting errors.\n\n"
            "Checklist item: Spelling, grammar, headings, dates, names, units, and "
            "formatting are consistent.\n\n"
            "In the financial statement review step, check consistency of terminology, "
            "dates, currencies, cross-references, spelling, and grammar."
        ),
        "topic": "spell_grammar",
        "page": 1,
        "source": "WP514_mentor_reference",
    },
]
