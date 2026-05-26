from fastapi import FastAPI

from app.api.routes import assets, aura, health, ingestion, pipelines
from app.core.settings import get_settings
from app.db.base import Base
from app.db.session import engine

settings = get_settings()
app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def on_startup() -> None:
	Base.metadata.create_all(bind=engine)

app.include_router(health.router, tags=["health"])
app.include_router(aura.router, prefix="/aura", tags=["aura"])
app.include_router(ingestion.router, prefix="/ingestion", tags=["ingestion"])
app.include_router(assets.router, tags=["assets"])
app.include_router(pipelines.router, tags=["pipelines"])
