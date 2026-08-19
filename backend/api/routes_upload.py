import os
import shutil
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from db.database import get_db
from db import crud
from config import STORAGE_DIR
from pipeline import run_pipeline

router = APIRouter()


@router.post("/upload")
async def upload_statement(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    linked_prior_statement_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
):
    filepath = os.path.join(STORAGE_DIR, file.filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    statement = crud.create_statement(
        db,
        filename=file.filename,
        filepath=filepath,
        linked_prior_statement_id=linked_prior_statement_id,
    )

    background_tasks.add_task(run_pipeline, statement.id)

    return {"id": statement.id, "status": statement.status}
