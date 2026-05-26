"""Routes for GL account and journal entries."""

from typing import Any

from fastapi import APIRouter, Depends

from ..client import BillitAPIClient
from ..dependencies import get_client

router = APIRouter()


@router.post("/gl-accounts")
async def create_gl_account(
    account_data: dict[str, Any], client: BillitAPIClient = Depends(get_client)
) -> dict[str, Any]:
    """Create a single GL account."""
    return await client.request("POST", "/glAccount", json=account_data)


@router.post("/gl-accounts/import")
async def import_gl_accounts(
    accounts_data: list[dict[str, Any]],
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Import multiple GL accounts."""
    return await client.request("POST", "/glAccount/import", json=accounts_data)


@router.post("/journal-entries/import")
async def import_journal_entries(
    entries_data: list[dict[str, Any]],
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Import journal entries."""
    return await client.request("POST", "/journalEntry/import", json=entries_data)
