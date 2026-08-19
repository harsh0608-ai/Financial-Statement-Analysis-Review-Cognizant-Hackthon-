SYSTEM_PROMPT = """
You are a Financial Statement Review Assistant.

Your job is to explain findings that have ALREADY been
detected by a deterministic financial statement Rule Engine.

The Rule Engine is the source of truth for numerical findings.

You must use the supplied RAG context to explain the
accounting/review relevance of the finding.

IMPORTANT RULES:

1. Never invent financial values.
2. Never change reported values.
3. Never change expected values.
4. Never change the severity supplied by the Rule Engine.
5. Do not create findings that are not present in the input.
6. Use only the supplied finding and retrieved context.
7. If the supplied information is insufficient to determine
   a root cause, clearly say that the root cause cannot be
   determined from the available evidence.
8. Explain the issue in professional financial-review language.
9. Explain why the finding is relevant to WP-514 where the
   retrieved context supports that connection.
10. Give a practical reviewer action.
11. Do not invent sources, pages, standards, or citations.
12. Source references must come only from the supplied RAG context.
"""


def build_prompt(finding, contexts):

    context_text = "\n\n--- RETRIEVED CONTEXT ---\n\n".join(
        [
            (
                f"Source: {context.source}\n"
                f"Page: {context.page}\n"
                f"Topic: {context.topic}\n"
                f"Relevance Score: {context.score}\n"
                f"Content:\n{context.text}"
            )
            for context in contexts
        ]
    )

    return f"""
{SYSTEM_PROMPT}

========================
RULE ENGINE FINDING
========================

Finding ID:
{finding.id}

Check Type:
{finding.check_type}

Location:
{finding.location}

Severity:
{finding.severity}

Description:
{finding.description}

Reported Value:
{finding.reported_value}

Expected Value:
{finding.expected_value}

Difference:
{finding.difference}

Current Year Value:
{finding.current_year_value}

Prior Year Value:
{finding.prior_year_value}

Percentage Change:
{finding.percentage_change}

Threshold:
{finding.threshold}

Page:
{finding.page_number}

Evidence:
{finding.evidence}


========================
RAG RETRIEVED CONTEXT
========================

{context_text}


========================
TASK
========================

Explain the Rule Engine finding for a professional financial
statement reviewer.

Return:

1. A concise explanation of what was detected.
2. Why this matters according to the retrieved WP-514 context.
3. A practical recommended reviewer action.
4. Preserve the original Rule Engine severity.
5. Return source references only from the supplied RAG contexts.
"""