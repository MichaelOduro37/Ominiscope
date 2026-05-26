import uuid
from typing import Any, Dict

from app.jobs.base import JobResult


def ingest_job(payload: Dict[str, Any]) -> JobResult:
    _ = payload
    return JobResult(
        status="completed",
        payload={
            "asset_id": str(uuid.uuid4()),
            "version_id": str(uuid.uuid4()),
            "cube_id": str(uuid.uuid4()),
        },
    )
