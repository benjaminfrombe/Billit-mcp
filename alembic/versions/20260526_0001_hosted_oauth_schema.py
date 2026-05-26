"""hosted oauth schema

Revision ID: 20260526_0001
Revises:
Create Date: 2026-05-26
"""

from __future__ import annotations

from alembic import op

from billit_mcp.persistence.models import Base

revision = "20260526_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create hosted OAuth tables."""

    bind = op.get_bind()
    Base.metadata.create_all(bind)


def downgrade() -> None:
    """Drop hosted OAuth tables."""

    bind = op.get_bind()
    Base.metadata.drop_all(bind)
