from ingestion.chunker import chunk_sections


def test_small_section_stays_together():
    sections = [{
        "section_id": "x",
        "title": "AR Days",
        "content": "Formula: Average AR / Revenue * 365\n\nExample: AR is 10 and revenue is 100.",
        "topic": "ratio_analysis",
        "page": 3,
        "source": "WP514_mentor_reference",
    }]
    chunks = chunk_sections(sections, chunk_size=50, overlap=5)
    assert len(chunks) == 1
    assert "Formula" in chunks[0]["text"]
    assert chunks[0]["metadata"]["topic"] == "ratio_analysis"
