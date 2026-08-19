import json

from sqlalchemy.orm import Session
from db.models import Statement, FinancialLineItem, Finding


def create_statement(
    db: Session, filename: str, filepath: str, linked_prior_statement_id: int = None,
) -> Statement:
    statement = Statement(
        filename=filename,
        filepath=filepath,
        status="queued",
        linked_prior_statement_id=linked_prior_statement_id,
    )
    db.add(statement)
    db.commit()
    db.refresh(statement)
    return statement


def update_statement_status(db: Session, statement_id: int, status: str) -> Statement:
    statement = db.query(Statement).filter(Statement.id == statement_id).first()
    if statement:
        statement.status = status
        db.commit()
        db.refresh(statement)
    return statement


def get_statement(db: Session, statement_id: int) -> Statement:
    return db.query(Statement).filter(Statement.id == statement_id).first()


def bulk_insert_line_items(db: Session, statement_id: int, items: list[dict]) -> list[FinancialLineItem]:
    objects = [
        FinancialLineItem(
            statement_id=statement_id,
            year=item.get("year"),
            statement_type=item.get("statement_type"),
            label=item.get("label"),
            value=item.get("value"),
            page_number=item.get("page_number"),
            table_id=item.get("table_id"),
            order_index=item.get("order_index"),
            is_total=item.get("is_total", False),
            group_id=item.get("group_id"),
        )
        for item in items
    ]
    db.add_all(objects)
    db.commit()
    return objects


def get_line_items(db: Session, statement_id: int, year: str = None) -> list[FinancialLineItem]:
    query = db.query(FinancialLineItem).filter(FinancialLineItem.statement_id == statement_id)
    if year:
        query = query.filter(FinancialLineItem.year == year)
    return query.all()


def bulk_insert_findings(db: Session, statement_id: int, findings: list[dict]) -> list[Finding]:
    objects = [
        Finding(
            statement_id=statement_id,
            check_type=f.get("check_type"),
            location=f.get("location"),
            severity=f.get("severity", "medium"),
            description=f.get("description", ""),
            reported_value=f.get("reported_value"),
            expected_value=f.get("expected_value"),
            difference=f.get("difference"),
            current_year_value=f.get("current_year_value"),
            prior_year_value=f.get("prior_year_value"),
            percentage_change=f.get("percentage_change"),
            threshold=f.get("threshold"),
            page_number=f.get("page_number"),
            evidence=json.dumps(f["evidence"]) if f.get("evidence") else None,
        )
        for f in findings
    ]
    db.add_all(objects)
    db.commit()
    return objects


def get_findings(db: Session, statement_id: int) -> list[Finding]:
    return db.query(Finding).filter(Finding.statement_id == statement_id).all()


def update_finding_explanation(db: Session, finding_id: int, explanation: str) -> Finding:
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    if finding:
        finding.explanation = explanation
        db.commit()
        db.refresh(finding)
    return finding


def finding_to_dict(f: Finding) -> dict:
    """Serialize a Finding row into the unified finding schema."""
    return {
        "id": f.id,
        "check_type": f.check_type,
        "location": f.location,
        "severity": f.severity,
        "description": f.description,
        "reported_value": f.reported_value,
        "expected_value": f.expected_value,
        "difference": f.difference,
        "current_year_value": f.current_year_value,
        "prior_year_value": f.prior_year_value,
        "percentage_change": f.percentage_change,
        "threshold": f.threshold,
        "page_number": f.page_number,
        "evidence": json.loads(f.evidence) if f.evidence else None,
        "explanation": f.explanation,
    }
