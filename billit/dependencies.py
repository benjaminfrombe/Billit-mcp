"""Shared FastAPI dependencies for Billit adapters."""

from collections.abc import AsyncIterator

from .client import BillitAPIClient, BillitSettings


def build_client(settings: BillitSettings | None = None) -> BillitAPIClient:
    """Return a configured Billit API client."""

    return BillitAPIClient(settings)


async def get_client() -> AsyncIterator[BillitAPIClient]:
    """Yield a request-scoped Billit API client."""

    client = build_client()
    try:
        yield client
    finally:
        await client.close()
