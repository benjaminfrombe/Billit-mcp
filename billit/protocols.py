"""Shared structural types for Billit service helpers."""

from __future__ import annotations

from typing import Any, Protocol


class BillitRequester(Protocol):
    """Minimal async request contract used by adapter-neutral helpers."""

    async def request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        """Perform a Billit API request and return the standard envelope."""
        ...
