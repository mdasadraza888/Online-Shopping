from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from sqlalchemy import ForeignKey, Numeric
from datetime import datetime
from decimal import Decimal

if TYPE_CHECKING:
    from .cart import Cart
    from .product import Product

class CartItem(Base):
    __tablename__ = 'cartitem'

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    variant_id: Mapped[int] = mapped_column(ForeignKey('productvariant.id'), nullable=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_snapshot: Mapped[Decimal] = mapped_column(Numeric(scale=2), nullable=False)

    cart: Mapped['Cart'] = relationship(back_populates='cartitem')
    product: Mapped['Product'] = relationship(back_populates='cartitem')