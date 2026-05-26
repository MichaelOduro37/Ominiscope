from fastapi import FastAPI

from app.api.routes import aura, health, ingestion
from app.core.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.include_router(health.router, tags=["health"])
app.include_router(aura.router, prefix="/aura", tags=["aura"])
app.include_router(ingestion.router, prefix="/ingestion", tags=["ingestion"])
