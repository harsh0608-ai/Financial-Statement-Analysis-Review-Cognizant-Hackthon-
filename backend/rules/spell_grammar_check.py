import logging

import language_tool_python

logger = logging.getLogger(__name__)

_tool = None


def get_tool():
    global _tool
    if _tool is None:
        _tool = language_tool_python.LanguageTool("en-US")
    return _tool


def run_spell_grammar_check(pages_text: list) -> list[dict]:
    findings = []

    try:
        tool = get_tool()
    except Exception:
        logger.exception("Could not initialize the spelling/grammar tool; skipping this check.")
        return findings

    for page in pages_text:
        text = page["text"]
        if not text or len(text.strip()) < 5:
            continue

        try:
            matches = tool.check(text)
        except Exception:
            logger.exception("Spelling/grammar check failed on page %s; skipping that page.", page["page_number"])
            continue

        for match in matches:
            findings.append({
                "check_type": "spell_grammar",
                "location": f"page {page['page_number']}",
                "severity": "low",
                "description": f"{match.message} (context: '{match.context}')",
                "page_number": page["page_number"],
            })

    return findings
