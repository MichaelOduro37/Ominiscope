from functools import lru_cache
import os

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "OmniScope API"
    env: str = "dev"
    database_url: str = "sqlite:///./omniscope.db"
    redis_url: str = os.getenv("OMNISCOPE_REDIS_URL", "redis://localhost:6379/0")
    queue_name: str = os.getenv("OMNISCOPE_QUEUE", "omniscope")


@lru_cache
def get_settings() -> Settings:
    return Settings()
