from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from sqlalchemy import ForeignKey, Enum as SqlEnum, Numeric, DateTime, func
from enum import Enum
from datetime import datetime
from .order_item import OrderItem
from .payment import Payment

class Status(str, Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[Status] = mapped_column(SqlEnum(Status), nullable=False)
    total: Mapped[float] = mapped_column(Numeric(scale=2), nullable=False)
    shipping_address_id: Mapped[int] = mapped_column(ForeignKey('address.id'))
    coupon_id: Mapped[int] = mapped_column(ForeignKey('coupon.id'), nullable=True)
    placed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    orderitem: Mapped[OrderItem] = relationship(back_populates='order')
    payment: Mapped[Payment] = relationship(back_populates='order')