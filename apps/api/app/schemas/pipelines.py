import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PipelineRunOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    orchestration_id: Optional[str] = None
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
