from __future__ import annotations

import datetime
import uuid
from typing import Any, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def _id() -> str:
    return str(uuid.uuid4())


class DataAsset(Base):
    __tablename__ = "data_assets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_id)
    name: Mapped[str] = mapped_column(String(255))
    source_type: Mapped[str] = mapped_column(String(50))
    owner_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    sensitivity: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    retention_policy_id: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True
    )

    versions: Mapped[list[DataVersion]] = relationship(
        "DataVersion", back_populates="asset", cascade="all, delete-orphan"
    )


class DataVersion(Base):
    __tablename__ = "data_versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_id)
    asset_id: Mapped[str] = mapped_column(ForeignKey("data_assets.id"))
    version_label: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    checksum: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    size_bytes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    raw_uri: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    ingested_by: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    mime_type: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    format: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    asset: Mapped[DataAsset] = relationship("DataAsset", back_populates="versions")
    cubes: Mapped[list[DataCube]] = relationship(
        "DataCube", back_populates="version", cascade="all, delete-orphan"
    )


class DataCube(Base):
    __tablename__ = "data_cubes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_id)
    version_id: Mapped[str] = mapped_column(ForeignKey("data_versions.id"))
    cube_type: Mapped[str] = mapped_column(String(64))
    shape: Mapped[Optional[list[int]]] = mapped_column(JSON, nullable=True)
    axes: Mapped[Optional[list[dict[str, Any]]]] = mapped_column(JSON, nullable=True)
    channels: Mapped[Optional[list[dict[str, Any]]]] = mapped_column(
        JSON, nullable=True
    )
    storage_uri: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    version: Mapped[DataVersion] = relationship("DataVersion", back_populates="cubes")


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_id)
    orchestration_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="queued")
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
