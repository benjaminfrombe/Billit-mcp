"""Routes for Billit financial transaction endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, UploadFile

from ..client import BillitAPIClient
from ..dependencies import get_client
from ..endpoints import FINANCIAL_TRANSACTIONS_ENDPOINT, list_params

router = APIRouter()


@router.get("/financial-transactions")
async def list_financial_transactions(
    odata_filter: str | None = None,
    skip: int = 0,
    top: int = 120,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Retrieve bank transactions."""
    params = list_params(skip=skip, top=top, odata_filter=odata_filter)
    return await client.request("GET", FINANCIAL_TRANSACTIONS_ENDPOINT, params=params)


@router.post("/financial-transactions/import")
async def import_transactions_file(
    file: UploadFile,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Upload a bank statement file."""
    files = {"file": (file.filename, await file.read())}
    return await client.request(
        "POST",
        f"{FINANCIAL_TRANSACTIONS_ENDPOINT}/importFile",
        files=files,
    )


@router.post("/financial-transactions/{import_id}/confirm")
async def confirm_transaction_import(
    import_id: str,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Confirm a transaction file import."""
    return await client.request("POST", f"{FINANCIAL_TRANSACTIONS_ENDPOINT}/commands/import")
