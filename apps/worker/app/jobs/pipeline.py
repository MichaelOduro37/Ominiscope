from typing import Any, Dict

from app.jobs.base import JobResult


def pipeline_job(payload: Dict[str, Any]) -> JobResult:
    _ = payload
    return JobResult(status="completed", payload={"result": "ok"})
