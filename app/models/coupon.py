from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from sqlalchemy import Enum as SqlEnum, Numeric, DateTime, text
from enum import Enum
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order

class CouponType(str, Enum):
    PERCENTAGE = 'percentage'
    FIXED_AMOUNT = 'fixed_amount'
    FREE_SHIPPING = 'free_shipping'

class Coupon(Base):
    __tablename__ = 'coupons'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True)
    type: Mapped[CouponType] = mapped_column(SqlEnum(CouponType, values_callable=lambda x: [e.value for e in x]), default=CouponType.FIXED_AMOUNT)
    value: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    expiry: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    usage_limit: Mapped[int | None] = mapped_column()
    min_order_value: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))

    order: Mapped[Order] = relationship(back_populates='coupon')