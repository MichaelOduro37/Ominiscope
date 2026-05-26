from functools import lru_cache
import os


class Settings:
    def __init__(self) -> None:
        self.redis_url = os.getenv("OMNISCOPE_REDIS_URL", "redis://localhost:6379/0")
        self.queue_name = os.getenv("OMNISCOPE_QUEUE", "omniscope")


@lru_cache
def get_settings() -> Settings:
    return Settings()
