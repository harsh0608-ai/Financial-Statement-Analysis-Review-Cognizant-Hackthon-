from __future__ import annotations


def normalize_metadata(metadata: dict) -> dict:
    """Normalize metadata into Chroma-safe primitive values."""
    out = {}
    for key, value in metadata.items():
        if value is None:
            continue
        if isinstance(value, (str, int, float, bool)):
            out[key] = value
        else:
            out[key] = str(value)
    return out
