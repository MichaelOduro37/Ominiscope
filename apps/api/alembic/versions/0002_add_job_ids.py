"""add job ids

Revision ID: 0002_add_job_ids
Revises: 0001_initial
Create Date: 2026-05-26
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_add_job_ids"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "data_versions", sa.Column("job_id", sa.String(length=64), nullable=True)
    )
    op.add_column(
        "pipeline_runs", sa.Column("job_id", sa.String(length=64), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("pipeline_runs", "job_id")
    op.drop_column("data_versions", "job_id")
