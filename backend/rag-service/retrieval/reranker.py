from __future__ import annotations

import re


def lexical_overlap(query: str, text: str) -> float:
    q = set(re.findall(r"[a-z0-9]+", query.lower()))
    t = set(re.findall(r"[a-z0-9]+", text.lower()))
    if not q or not t:
        return 0.0
    return len(q & t) / len(q)


def rerank(rows: list[dict], query: str, preferred_topic: str) -> list[dict]:
    """Small deterministic tie-breaker; semantic similarity remains dominant."""
    for row in rows:
        topic_bonus = 0.05 if row.get("metadata", {}).get("topic") == preferred_topic else 0.0
        lexical_bonus = 0.05 * lexical_overlap(query, row.get("text", ""))
        row["score"] = min(1.0, row["score"] + topic_bonus + lexical_bonus)
    return sorted(rows, key=lambda x: x["score"], reverse=True)
