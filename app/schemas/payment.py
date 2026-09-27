from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from app.models.payment import PaymentStatus, PaymentMethod

class PaymentRequest(BaseModel):
    method: PaymentMethod

class PaymentResponse(BaseModel):
    id: int
    order_id: int
    gateway: str
    gateway_txn_id: str | None
    status: PaymentStatus
    amount: Decimal
    method: str

    model_config = ConfigDict(from_attributes=True)

