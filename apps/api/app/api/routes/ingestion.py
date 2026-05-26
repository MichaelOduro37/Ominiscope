from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import models
from app.db.deps import get_db
from app.schemas.ingestion import IngestRequest, IngestResponse
from app.worker_queue import enqueue_job

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
def ingest(payload: IngestRequest, db: Session = Depends(get_db)) -> IngestResponse:
    metadata = payload.metadata or {}
    asset = models.DataAsset(
        name=payload.name,
        source_type=payload.source_type,
        owner_id=metadata.get("owner_id"),
        tags=metadata.get("tags", []),
        sensitivity=metadata.get("sensitivity"),
        retention_policy_id=metadata.get("retention_policy_id"),
    )
    version = models.DataVersion(
        asset=asset,
        version_label=metadata.get("version_label", "v1"),
        checksum=metadata.get("checksum"),
        size_bytes=metadata.get("size_bytes"),
        raw_uri=metadata.get("raw_uri"),
        ingested_by=metadata.get("ingested_by"),
        mime_type=metadata.get("mime_type"),
        format=metadata.get("format"),
    )
    cube = models.DataCube(
        version=version,
        cube_type=metadata.get("cube_type", "document"),
        shape=metadata.get("shape"),
        axes=metadata.get("axes"),
        channels=metadata.get("channels"),
        storage_uri=metadata.get("storage_uri"),
    )
    db.add(asset)
    db.add(version)
    db.add(cube)
    db.commit()
    db.refresh(asset)
    db.refresh(version)
    db.refresh(cube)

    try:
        job_id = enqueue_job(
            "app.jobs.ingest.ingest_job",
            {
                "asset_id": asset.id,
                "version_id": version.id,
                "cube_id": cube.id,
            },
        )
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=503, detail="Worker queue unavailable") from exc

    version.job_id = job_id
    db.commit()
    db.refresh(version)
    return IngestResponse(
        asset_id=asset.id,
        version_id=version.id,
        cube_id=cube.id,
        job_id=job_id,
    )
