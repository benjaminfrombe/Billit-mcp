"""Routes for Billit report generation."""

from typing import Any

from fastapi import APIRouter, Depends, Request

from ..client import BillitAPIClient
from ..dependencies import get_client
from ..endpoints import report_endpoint

router = APIRouter()


@router.get("/reports")
async def list_available_reports(
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """List all report types."""
    return await client.request("GET", report_endpoint())


@router.get("/reports/{report_id}")
async def get_report(
    report_id: str,
    request: Request,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """Retrieve a specific report."""
    # Pass through any query parameters
    params = dict(request.query_params)
    return await client.request("GET", report_endpoint(report_id), params=params)
