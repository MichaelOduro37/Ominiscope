from fastapi import APIRouter

from app.schemas.ingestion import IngestRequest, IngestResponse

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
def ingest(payload: IngestRequest) -> IngestResponse:
    _ = payload
    return IngestResponse(asset_id="a_stub", version_id="v_stub", cube_id="c_stub")
