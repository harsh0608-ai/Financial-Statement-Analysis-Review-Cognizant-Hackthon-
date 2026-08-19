import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from db.database import get_db
from db import crud
from config import REPORT_DIR

router = APIRouter()


@router.get("/report/{statement_id}")
def get_report(statement_id: int, db: Session = Depends(get_db)):
    statement = crud.get_statement(db, statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")

    if statement.status != "done":
        raise HTTPException(status_code=400, detail=f"Report not ready. Current status: {statement.status}")

    report_path = os.path.join(REPORT_DIR, f"report_{statement_id}.html")

    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report file not found")

    return FileResponse(report_path, media_type="text/html", filename=f"audit_report_{statement_id}.html")
