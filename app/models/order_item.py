from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from sqlalchemy import ForeignKey, Enum as SqlEnum, Numeric, DateTime, func
from enum import Enum
from datetime import datetime
from decimal import Decimal
from .order import Order
from .product import Product

class OrderItem(Base):
    __tablename__ = 'orderitem'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_at_purchase: Mapped[Decimal] = mapped_column(Numeric(scale=2), nullable=False)

    order: Mapped[Order] = relationship(back_populates='orderitem')
    product: Mapped[Product] = relationship(back_populates='orderitem')
    