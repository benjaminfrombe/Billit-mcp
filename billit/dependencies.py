"""Shared FastAPI dependencies for Billit adapters."""

from collections.abc import AsyncIterator

from .client import BillitAPIClient


def build_client() -> BillitAPIClient:
    """Return a configured Billit API client."""

    return BillitAPIClient()


async def get_client() -> AsyncIterator[BillitAPIClient]:
    """Yield a request-scoped Billit API client."""

    client = build_client()
    try:
        yield client
    finally:
        await client.close()
