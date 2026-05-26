import redis
from rq import Queue

from app.config import get_settings

_settings = get_settings()


def get_connection() -> redis.Redis:
    return redis.Redis.from_url(_settings.redis_url)


def get_queue() -> Queue:
    return Queue(_settings.queue_name, connection=get_connection())
