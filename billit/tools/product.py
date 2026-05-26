"""FastAPI routes for Billit Product endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from ..client import BillitAPIClient
from ..dependencies import get_client
from ..models.product import ProductUpsert

router = APIRouter()


@router.get("/products")
async def list_products(
    odata_filter: str | None = None,
    skip: int = 0,
    top: int = 120,
    client: BillitAPIClient = Depends(get_client),
) -> dict[str, Any]:
    """List products with optional OData filter and pagination."""

    params: dict[str, Any] = {"$skip": skip, "$top": top}
    if odata_filter:
        params["$filter"] = odata_filter
    return await client.request("GET", "/products", params=params)


@router.get("/products/{product_id}")
async def get_product(
    product_id: int, client: BillitAPIClient = Depends(get_client)
) -> dict[str, Any]:
    """Fetch a single product by ID."""

    return await client.request("GET", f"/products/{product_id}")


@router.post("/products")
async def upsert_product(
    product_data: dict[str, Any], client: BillitAPIClient = Depends(get_client)
) -> dict[str, Any]:
    """Create or update a product."""

    try:
        product = ProductUpsert.model_validate(product_data)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc
    data = product.model_dump(exclude_none=True, by_alias=True)
    return await client.request("POST", "/products", json=data)
