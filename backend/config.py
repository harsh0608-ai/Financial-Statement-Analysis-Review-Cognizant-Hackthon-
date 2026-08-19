import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/audit_db"
)

RAG_SERVICE_URL = os.getenv(
    "RAG_SERVICE_URL",
    "http://localhost:8001/retrieve"
)

GENAI_SERVICE_URL = os.getenv(
    "GENAI_SERVICE_URL",
    "http://localhost:8002/explain"
)

STORAGE_DIR = os.getenv(
    "STORAGE_DIR",
    os.path.join(os.path.dirname(__file__), "storage", "files")
)

REPORT_DIR = os.getenv(
    "REPORT_DIR",
    os.path.join(os.path.dirname(__file__), "storage", "reports")
)

# Minimum absolute percentage movement (current year vs prior year)
# that the analytical review check flags for investigation.
ANALYTICAL_THRESHOLD_PERCENT = float(
    os.getenv("ANALYTICAL_THRESHOLD_PERCENT", "10")
)

os.makedirs(STORAGE_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)