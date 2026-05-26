"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-05-26
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "data_assets",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("source_type", sa.String(length=50), nullable=False),
        sa.Column("owner_id", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("sensitivity", sa.String(length=32), nullable=True),
        sa.Column("retention_policy_id", sa.String(length=64), nullable=True),
    )

    op.create_table(
        "data_versions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("asset_id", sa.String(length=36), nullable=False),
        sa.Column("version_label", sa.String(length=32), nullable=True),
        sa.Column("checksum", sa.String(length=128), nullable=True),
        sa.Column("size_bytes", sa.Integer(), nullable=True),
        sa.Column("raw_uri", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("ingested_by", sa.String(length=64), nullable=True),
        sa.Column("mime_type", sa.String(length=128), nullable=True),
        sa.Column("format", sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(["asset_id"], ["data_assets.id"]),
    )

    op.create_table(
        "data_cubes",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("version_id", sa.String(length=36), nullable=False),
        sa.Column("cube_type", sa.String(length=64), nullable=False),
        sa.Column("shape", sa.JSON(), nullable=True),
        sa.Column("axes", sa.JSON(), nullable=True),
        sa.Column("channels", sa.JSON(), nullable=True),
        sa.Column("storage_uri", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["version_id"], ["data_versions.id"]),
    )

    op.create_table(
        "pipeline_runs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("orchestration_id", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("pipeline_runs")
    op.drop_table("data_cubes")
    op.drop_table("data_versions")
    op.drop_table("data_assets")
