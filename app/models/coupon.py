from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from sqlalchemy import ForeignKey, Enum as SqlEnum, Numeric, DateTime, func
from enum import Enum
from datetime import datetime
from decimal import Decimal
from .order import Order

class CouponType(str, Enum):
    PERCENTAGE = 'percentage'
    FIXED_AMOUNT = 'fixed_amount'
    FREE_SHIPPING = 'free_shipping'

class Coupon(Base):
    __tablename__ = 'coupon'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True)
    type: Mapped[str]
    value: Mapped[Decimal] = mapped_column(Numeric(scale=2), nullable=False)
    expiry: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    usage_limit: Mapped[int | None] = mapped_column()
    min_order_value: Mapped[Decimal] = mapped_column(Numeric(scale=2))

    order: Mapped[Order] = relationship(back_populates='coupon')