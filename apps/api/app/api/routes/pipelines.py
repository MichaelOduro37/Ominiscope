from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import models
from app.db.deps import get_db
from app.schemas.pipelines import PipelineRunOut
from app.worker_queue import get_job_status

router = APIRouter()


@router.get("/pipelines/{pipeline_id}", response_model=PipelineRunOut)
def get_pipeline(pipeline_id: str, db: Session = Depends(get_db)) -> PipelineRunOut:
    pipeline = db.get(models.PipelineRun, pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    if pipeline.job_id:
        job_status = get_job_status(pipeline.job_id)
        status_map = {
            "queued": "queued",
            "started": "running",
            "finished": "completed",
            "failed": "failed",
            "deferred": "queued",
            "scheduled": "queued",
        }
        if job_status:
            mapped = status_map.get(job_status, pipeline.status)
            if mapped != pipeline.status:
                pipeline.status = mapped
                pipeline.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(pipeline)
    return pipeline
