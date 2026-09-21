from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from sqlalchemy import ForeignKey, Numeric, DateTime, func, Text
from decimal import Decimal
from datetime import datetime

if TYPE_CHECKING:
    from .category import Category
    from .productvariant import ProductVariant
    from .review import Review

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2),nullable=False)
    sku: Mapped[str] = mapped_column(unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    stock: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    category: Mapped['Category'] = relationship(back_populates='products')
    productvariants: Mapped[list['ProductVariant']] = relationship(back_populates='product')
    reviews: Mapped[list['Review']] = relationship(back_populates='product')