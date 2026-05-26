import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import models
from app.db.deps import get_db
from app.schemas.aura import OrchestrationRequest, OrchestrationResponse

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
    return OrchestrationResponse(
        orchestration_id=orchestration_id,
        pipeline_id=pipeline.id,
        status=pipeline.status,
        next_action="none",
    )
