from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import models
from app.db.deps import get_db
from app.schemas.pipelines import PipelineRunOut

router = APIRouter()


@router.get("/pipelines/{pipeline_id}", response_model=PipelineRunOut)
def get_pipeline(pipeline_id: str, db: Session = Depends(get_db)) -> PipelineRunOut:
    pipeline = db.get(models.PipelineRun, pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline
