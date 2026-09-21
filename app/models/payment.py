from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from sqlalchemy import ForeignKey, Enum as SqlEnum, Numeric
from enum import Enum
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order

class PaymentStatus(str, Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    REFUNDED = 'refunded'
    DISPUTED = 'disputed'

class Payment(Base):
    __tablename__ = 'payments'
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), unique=True, nullable=False)
    gateway: Mapped[str]
    gateway_txn_id: Mapped[str | None] = mapped_column(unique=True)
    status: Mapped[PaymentStatus] = mapped_column(SqlEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    method: Mapped[str] = mapped_column(nullable=False)

    order: Mapped[Order] = relationship(back_populates='payment')