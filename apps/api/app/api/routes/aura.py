import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import models
from app.db.deps import get_db
from app.schemas.aura import OrchestrationRequest, OrchestrationResponse
from app.worker_queue import enqueue_job

router = APIRouter()


@router.post("/orchestrations", response_model=OrchestrationResponse)
def create_orchestration(
    payload: OrchestrationRequest, db: Session = Depends(get_db)
) -> OrchestrationResponse:
    _ = payload
    orchestration_id = str(uuid.uuid4())
    pipeline = models.PipelineRun(
        orchestration_id=orchestration_id,
        status="queued",
    )
    db.add(pipeline)
    db.commit()
    db.refresh(pipeline)

    try:
        job_id = enqueue_job(
            "app.jobs.pipeline.pipeline_job",
            {"pipeline_id": pipeline.id},
        )
    except Exception as exc:
        pipeline.status = "failed"
        db.commit()
        raise HTTPException(status_code=503, detail="Worker queue unavailable") from exc

    pipeline.job_id = job_id
    db.commit()
    db.refresh(pipeline)
    return OrchestrationResponse(
        orchestration_id=orchestration_id,
        pipeline_id=pipeline.id,
        status=pipeline.status,
        next_action="none",
        job_id=job_id,
    )
