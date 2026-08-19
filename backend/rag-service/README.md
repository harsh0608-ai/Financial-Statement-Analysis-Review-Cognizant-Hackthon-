# WP-514 Financial Statement RAG Service

Standalone retrieval service for the financial-statement review system. It consumes structured findings from the existing backend and retrieves relevant mentor-provided WP-514 guidance. It does **not** generate explanations and does not require a Gemini/LLM API key.

## Architecture

`Finding JSON -> query builder -> local embeddings -> ChromaDB -> retrieved WP-514 chunks -> JSON`

The future GenAI service can consume the returned contexts.

## Setup

From this directory:

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
```

## Build the knowledge index

The mentor images are represented by a carefully verified transcript in `knowledge_base/wp514/verified_content.py`. This avoids blindly indexing OCR errors from the photographed source.

```bash
python -m ingestion.indexer
```

## Run

```bash
uvicorn app:app --host 0.0.0.0 --port 8001
```

Health check: `GET /health`

## Retrieve

`POST /retrieve`

Example:

```json
{
  "findings": [
    {
      "id": 1,
      "check_type": "mathematical_accuracy",
      "location": "Balance Sheet / Total Assets",
      "severity": "high",
      "description": "Reported Total Assets differs from calculated Total Assets",
      "reported_value": 170,
      "expected_value": 165,
      "difference": 5,
      "page_number": 1
    }
  ]
}
```

The response contains retrieved text plus `source`, `page`, `topic`, and relevance `score`. The service never calls an LLM.

## Backend integration

The existing backend can later POST its Finding objects to:

`http://localhost:8001/retrieve`

The existing `backend/integration/rag_client.py` remains the integration placeholder and is not required to run this service independently.

## Test

```bash
pytest -q
```

The dummy financial statements are test inputs for the existing backend/rule engine; they are not the permanent RAG knowledge base.
