from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    name: str = Field(..., min_length=1)
    source_type: str = Field(..., min_length=1)
    metadata: Optional[Dict[str, Any]] = None


class IngestResponse(BaseModel):
    asset_id: str
    version_id: str
    cube_id: str
    job_id: Optional[str] = None
