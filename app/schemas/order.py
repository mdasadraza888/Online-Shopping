from pydantic import BaseModel
from decimal import Decimal
from app.models.order import OrderStatus


class OrderItemRequest(BaseModel):
    product_id: int
    quantity: int

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price_at_purchase: Decimal

class OrderRequest(BaseModel):
    shipping_address_id: int
    coupon_id: int | None = None

class OrderUpdate(BaseModel):
    shipping_address_id: int | None = None

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    total: Decimal
    shipping_address_id: int
    coupon_id: int | None = None
    items: list[OrderItemResponse]