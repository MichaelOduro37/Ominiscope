import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DataAssetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    source_type: str
    created_at: datetime.datetime
    tags: list[str]
    sensitivity: Optional[str] = None
