from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from sqlalchemy import ForeignKey, Enum as SqlEnum, Numeric, DateTime, func
from enum import Enum
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order_item import OrderItem
    from .payment import Payment
    from .coupon import Coupon

class OrderStatus(str, Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PROCESSING = "processing"
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    RETURNED = "returned"

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[OrderStatus] = mapped_column(SqlEnum(OrderStatus, values_collable = lambda x: [e.value for e in x]), nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    shipping_address_id: Mapped[int] = mapped_column(ForeignKey('addresses.id'))
    coupon_id: Mapped[int] = mapped_column(ForeignKey('coupons.id'), nullable=True)
    placed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    order_item: Mapped[OrderItem] = relationship(back_populates='order', cascade="all, delete-orphan")
    payment: Mapped[Payment] = relationship(back_populates='order')
    coupon: Mapped["Coupon | None"] = relationship(back_populates="order")
