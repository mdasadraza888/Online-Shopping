from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal

class CartItemReqest(BaseModel):
    product_id: int
    variant_it: int
    quantity: int = Field(gt=0)

class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    variant_id: int | None
    quantity: int
    price_snapshot: Decimal

    model_config = ConfigDict(from_attributes=True)

class CartResponse(BaseModel):
    id: int
    items: list[CartItemResponse]

    model_config = ConfigDict(from_attributes=True)