"""Database helpers for hosted Billit MCP mode."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .models import Base

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


class HostedDatabase:
    """Small wrapper around the hosted async SQLAlchemy engine."""

    def __init__(self, database_url: str) -> None:
        """Create a hosted database handle."""

        if database_url.startswith("sqlite+aiosqlite:///"):
            path = database_url.removeprefix("sqlite+aiosqlite:///")
            if path and path != ":memory:":
                Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.engine: AsyncEngine = create_async_engine(database_url)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

    async def create_all_for_tests_only(self) -> None:
        """Create all hosted tables for isolated tests that do not exercise migrations."""

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def ping(self) -> None:
        """Run a cheap database connectivity check."""

        async with self.engine.connect() as conn:
            await conn.execute(text("select 1"))

    async def alembic_revision(self) -> str | None:
        """Return the current Alembic revision, or None when migrations are absent."""

        async with self.engine.connect() as conn:
            result = await conn.execute(text("select version_num from alembic_version"))
            value = result.scalar_one_or_none()
            return str(value) if value is not None else None

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Yield an async session with commit/rollback behavior."""

        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def close(self) -> None:
        """Dispose of database connections."""

        await self.engine.dispose()
