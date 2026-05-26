"""Explicit migration entrypoint for hosted Billit MCP persistence."""

from __future__ import annotations

import os
from pathlib import Path

from alembic import command
from alembic.config import Config

HOSTED_ALEMBIC_HEAD = "20260526_0001"


def project_root() -> Path:
    """Return the repository root for Alembic configuration."""

    return Path(__file__).resolve().parents[3]


def alembic_config(database_url: str | None = None) -> Config:
    """Build an Alembic config for the hosted persistence schema."""

    root = project_root()
    config = Config(str(root / "alembic.ini"))
    config.set_main_option("script_location", str(root / "alembic"))
    if database_url:
        config.set_main_option("sqlalchemy.url", database_url)
    return config


def run_migrations(database_url: str | None = None) -> None:
    """Upgrade hosted persistence to the current head revision."""

    if database_url:
        os.environ["BILLIT_MCP_DATABASE_URL"] = database_url
    command.upgrade(alembic_config(database_url), "head")


def stamp_migrations(database_url: str | None = None, revision: str = "head") -> None:
    """Stamp an already-compatible hosted schema with an Alembic revision."""

    if database_url:
        os.environ["BILLIT_MCP_DATABASE_URL"] = database_url
    command.stamp(alembic_config(database_url), revision)


def main() -> None:
    """CLI entrypoint for private-RDS-capable one-shot migration tasks."""

    run_migrations(os.getenv("BILLIT_MCP_DATABASE_URL"))


if __name__ == "__main__":
    main()
