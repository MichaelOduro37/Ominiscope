from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class OrchestrationContext(BaseModel):
    data_refs: Optional[List[Dict[str, str]]] = None
    constraints: Optional[Dict[str, Any]] = None
    persona: Optional[str] = None
    risk_level: Optional[str] = None


class OrchestrationRequest(BaseModel):
    request_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    goal: str = Field(..., min_length=1)
    context: Optional[OrchestrationContext] = None


class OrchestrationResponse(BaseModel):
    orchestration_id: str
    pipeline_id: str
    status: str
    next_action: str
    job_id: Optional[str] = None
