from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import models
from app.db.deps import get_db
from app.schemas.assets import DataAssetOut

router = APIRouter()


@router.get("/assets", response_model=list[DataAssetOut])
def list_assets(db: Session = Depends(get_db)) -> list[DataAssetOut]:
    return (
        db.query(models.DataAsset)
        .order_by(models.DataAsset.created_at.desc())
        .limit(50)
        .all()
    )
