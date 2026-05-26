from fastapi import APIRouter

from app.schemas.aura import OrchestrationRequest, OrchestrationResponse

router = APIRouter()


@router.post("/orchestrations", response_model=OrchestrationResponse)
def create_orchestration(payload: OrchestrationRequest) -> OrchestrationResponse:
    _ = payload
    return OrchestrationResponse(
        orchestration_id="o_stub",
        pipeline_id="p_stub",
        status="queued",
        next_action="none",
    )
