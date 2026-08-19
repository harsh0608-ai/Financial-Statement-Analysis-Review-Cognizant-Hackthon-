import asyncio
import logging

from db.database import SessionLocal
from db import crud
from extraction.pdf_parser import extract_raw_content
from extraction.normalizer import normalize_extraction
from rules.engine import run_all_checks
from integration.rag_client import get_explanations
from report.report_builder import build_report_html
from config import ANALYTICAL_THRESHOLD_PERCENT

logger = logging.getLogger(__name__)

YEAR_COLUMNS = ["current_year", "prior_year"]


def run_pipeline(statement_id: int):
    db = SessionLocal()

    try:
        statement = crud.get_statement(db, statement_id)
        if not statement:
            return

        crud.update_statement_status(db, statement_id, "extracting")

        raw_content = extract_raw_content(statement.filepath)
        structured_items = normalize_extraction(raw_content, YEAR_COLUMNS)
        crud.bulk_insert_line_items(db, statement_id, structured_items)

        crud.update_statement_status(db, statement_id, "reviewing")

        line_items = crud.get_line_items(db, statement_id)

        # If this statement was uploaded with a link to a previously
        # reviewed (signed) statement, pull that statement's "current
        # year" figures to use as the prior-year tie-out source.
        prior_statement_items = []
        if statement.linked_prior_statement_id:
            prior_statement_items = crud.get_line_items(
                db, statement.linked_prior_statement_id, year="current_year",
            )

        raw_findings = run_all_checks(
            line_items,
            raw_content["pages_text"],
            prior_statement_items=prior_statement_items,
            analytical_threshold_percent=ANALYTICAL_THRESHOLD_PERCENT,
        )
        crud.bulk_insert_findings(db, statement_id, raw_findings)

        findings = crud.get_findings(db, statement_id)

        try:
            explanations = asyncio.run(get_explanations(findings))
            explanation_map = explanations.get("explanations", {})

            for finding in findings:
                explanation_text = explanation_map.get(str(finding.id))
                if explanation_text:
                    crud.update_finding_explanation(db, finding.id, explanation_text)
        except Exception:
            # The AI-explanation service is out of scope for this phase
            # and must never block the deterministic review pipeline --
            # but the failure is still logged rather than swallowed.
            logger.warning(
                "RAG explanation service unavailable for statement %s; "
                "continuing without AI-generated explanations.",
                statement_id, exc_info=True,
            )

        findings = crud.get_findings(db, statement_id)
        build_report_html(statement, findings)

        crud.update_statement_status(db, statement_id, "done")

    except Exception:
        logger.exception("Pipeline failed for statement %s", statement_id)
        crud.update_statement_status(db, statement_id, "failed")
        raise

    finally:
        db.close()
