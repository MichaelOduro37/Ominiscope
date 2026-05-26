from functools import lru_cache

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "OmniScope API"
    env: str = "dev"
    database_url: str = "sqlite:///./omniscope.db"


@lru_cache
def get_settings() -> Settings:
    return Settings()
