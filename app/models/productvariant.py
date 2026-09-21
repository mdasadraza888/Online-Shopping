from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from sqlalchemy import ForeignKey, Numeric
from decimal import Decimal

if TYPE_CHECKING:
    from .product import Product

class ProductVariant(Base):
    __tablename__ = 'productvariants'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    size: Mapped[str] = mapped_column(nullable=True)
    color: Mapped[str] = mapped_column(nullable=True)
    price_override: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    stock: Mapped[int] = mapped_column(default=0)

    product: Mapped['Product'] = relationship(back_populates='productvariants')