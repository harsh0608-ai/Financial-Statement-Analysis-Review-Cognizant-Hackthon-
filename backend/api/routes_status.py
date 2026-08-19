from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import crud

router = APIRouter()


@router.get("/status/{statement_id}")
def get_status(statement_id: int, db: Session = Depends(get_db)):
    statement = crud.get_statement(db, statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")

    return {"id": statement.id, "filename": statement.filename, "status": statement.status}
