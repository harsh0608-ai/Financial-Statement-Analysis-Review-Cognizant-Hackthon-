"""Seeds a local SQLite database with realistic sample data for hackathon
testing -- three statements run through the REAL extraction/normalization/
rule-engine pipeline (not hand-typed fixtures), plus two placeholder rows to
exercise the /status endpoint's non-"done" states.

Usage:
    cd backend
    python3 dummy_data/seed_dummy_data.py

By default this creates ./dummy_finstatement.db (SQLite) next to wherever you
run it from. To point the real API at it:

    export DATABASE_URL="sqlite:///$(pwd)/dummy_finstatement.db"
    uvicorn main:app --reload

(If DATABASE_URL is already set in your environment when you run this
script, that target is used instead -- so you can seed a real Postgres
instance the same way, as long as it's reachable.)

Re-running this script wipes and recreates the DB from scratch, so it's
always safe to re-seed.
"""
import os
import shutil
import sys

DUMMY_DATA_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(DUMMY_DATA_DIR)
sys.path.insert(0, BACKEND_DIR)

DEFAULT_DB_PATH = os.path.join(os.getcwd(), "dummy_finstatement.db")
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = f"sqlite:///{DEFAULT_DB_PATH}"
    if os.path.exists(DEFAULT_DB_PATH):
        os.remove(DEFAULT_DB_PATH)

# Everything below must be imported AFTER DATABASE_URL is set.
from config import ANALYTICAL_THRESHOLD_PERCENT, STORAGE_DIR, REPORT_DIR  # noqa: E402
from db.database import Base, SessionLocal, engine  # noqa: E402
from db import crud  # noqa: E402
from extraction.pdf_parser import extract_raw_content  # noqa: E402
from extraction.normalizer import normalize_extraction  # noqa: E402
from rules.engine import run_all_checks  # noqa: E402
from report.report_builder import build_report_html  # noqa: E402

from generate_pdfs import PRIOR_PATH, CLEAN_PATH, BROKEN_PATH  # noqa: E402

YEAR_COLUMNS = ["current_year", "prior_year"]


def _copy_into_storage(source_path: str) -> str:
    filename = os.path.basename(source_path)
    dest_path = os.path.join(STORAGE_DIR, filename)
    shutil.copyfile(source_path, dest_path)
    return dest_path


def _process_statement(db, filename, source_path, linked_prior_statement_id=None):
    filepath = _copy_into_storage(source_path)
    statement = crud.create_statement(
        db, filename=filename, filepath=filepath,
        linked_prior_statement_id=linked_prior_statement_id,
    )

    crud.update_statement_status(db, statement.id, "extracting")
    raw_content = extract_raw_content(filepath)
    structured_items = normalize_extraction(raw_content, YEAR_COLUMNS)
    crud.bulk_insert_line_items(db, statement.id, structured_items)

    crud.update_statement_status(db, statement.id, "reviewing")
    line_items = crud.get_line_items(db, statement.id)

    prior_statement_items = []
    if linked_prior_statement_id:
        prior_statement_items = crud.get_line_items(
            db, linked_prior_statement_id, year="current_year",
        )

    findings = run_all_checks(
        line_items, raw_content["pages_text"],
        prior_statement_items=prior_statement_items,
        analytical_threshold_percent=ANALYTICAL_THRESHOLD_PERCENT,
    )
    crud.bulk_insert_findings(db, statement.id, findings)

    stored_findings = crud.get_findings(db, statement.id)
    build_report_html(statement, stored_findings)

    crud.update_statement_status(db, statement.id, "done")

    return statement, stored_findings


def main():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    summary = []

    try:
        prior_statement, prior_findings = _process_statement(
            db, "signed_prior_year_FY2025.pdf", PRIOR_PATH,
        )
        summary.append(("Signed prior-year baseline (FY2025)", prior_statement, prior_findings))

        clean_statement, clean_findings = _process_statement(
            db, "current_year_clean_FY2026.pdf", CLEAN_PATH,
            linked_prior_statement_id=prior_statement.id,
        )
        summary.append(("Clean current-year filing (FY2026)", clean_statement, clean_findings))

        broken_statement, broken_findings = _process_statement(
            db, "current_year_with_errors_FY2026.pdf", BROKEN_PATH,
            linked_prior_statement_id=prior_statement.id,
        )
        summary.append(("Current-year filing WITH ERRORS (FY2026)", broken_statement, broken_findings))

        # Two placeholder rows so /status/{id} has non-"done" examples too.
        queued = crud.create_statement(
            db, filename="just_uploaded_not_processed_yet.pdf",
            filepath=os.path.join(STORAGE_DIR, "just_uploaded_not_processed_yet.pdf"),
        )
        failed = crud.create_statement(
            db, filename="corrupted_upload.pdf",
            filepath=os.path.join(STORAGE_DIR, "corrupted_upload.pdf"),
        )
        crud.update_statement_status(db, failed.id, "failed")

        # Pull out plain values while the session is still open -- the
        # ORM objects above become unusable once db.close() runs below.
        rows = [
            (description, statement.id, statement.status, statement.filename, len(findings))
            for description, statement, findings in summary
        ]
        queued_row = (queued.id, queued.status, queued.filename)
        failed_row = (failed.id, failed.status, failed.filename)

    finally:
        db.close()

    print(f"\nSeeded database at: {os.environ['DATABASE_URL']}")
    print(f"Reports written to: {REPORT_DIR}\n")
    print(f"{'ID':<4} {'Status':<10} {'Findings':<9} Filename / description")
    print("-" * 78)
    for description, statement_id, status, filename, finding_count in rows:
        print(f"{statement_id:<4} {status:<10} {finding_count:<9} {filename}  ({description})")
    print(f"{queued_row[0]:<4} {queued_row[1]:<10} {'-':<9} {queued_row[2]}  (queued, not yet processed)")
    print(f"{failed_row[0]:<4} {failed_row[1]:<10} {'-':<9} {failed_row[2]}  (simulated failure)")

    print("\nSample requests once the API is running against this DB:")
    for description, statement_id, status, filename, finding_count in rows:
        print(f"  GET /findings/{statement_id}   -> {description}")
        print(f"  GET /report/{statement_id}     -> HTML report for the same statement")
    print(f"  GET /status/{queued_row[0]}        -> queued (not yet processed)")
    print(f"  GET /status/{failed_row[0]}        -> failed (simulated)")


if __name__ == "__main__":
    main()
