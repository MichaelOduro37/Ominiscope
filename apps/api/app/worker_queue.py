from typing import Any, Dict, Optional

import redis
from rq import Queue
from rq.job import Job

from app.core.settings import get_settings

_settings = get_settings()


def get_queue() -> Queue:
    connection = redis.Redis.from_url(_settings.redis_url)
    return Queue(_settings.queue_name, connection=connection)


def enqueue_job(func_path: str, payload: Dict[str, Any]) -> str:
    queue = get_queue()
    job = queue.enqueue(func_path, payload)
    return job.id


def get_job_status(job_id: str) -> Optional[str]:
    queue = get_queue()
    try:
        job = Job.fetch(job_id, connection=queue.connection)
    except Exception:
        return None
    return job.get_status()
