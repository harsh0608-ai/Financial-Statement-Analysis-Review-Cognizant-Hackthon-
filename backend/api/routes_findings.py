from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import crud

router = APIRouter()


@router.get("/findings/{statement_id}")
def get_findings(statement_id: int, db: Session = Depends(get_db)):
    statement = crud.get_statement(db, statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")

    findings = crud.get_findings(db, statement_id)

    return {
        "statement_id": statement_id,
        "count": len(findings),
        "findings": [crud.finding_to_dict(f) for f in findings],
    }
