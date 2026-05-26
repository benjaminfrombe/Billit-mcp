from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class Product(BaseModel):
    """Represents a product or service defined in Billit."""

    product_id: Annotated[int, Field(alias="ProductID")]
    description: Annotated[str, Field(alias="Description")]

    model_config = ConfigDict(populate_by_name=True)


class ProductUpsert(BaseModel):
    """Model used for creating or updating a product."""

    product_id: Annotated[int | None, Field(alias="ProductID")] = None
    description: Annotated[str, Field(alias="Description")]

    model_config = ConfigDict(populate_by_name=True)
