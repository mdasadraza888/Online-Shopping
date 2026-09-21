from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from sqlalchemy import ForeignKey, Numeric
from decimal import Decimal

if TYPE_CHECKING:
    from .cart import Cart
    from .product import Product

class CartItem(Base):
    __tablename__ = 'cartitems'

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    variant_id: Mapped[int] = mapped_column(ForeignKey('productvariants.id'), nullable=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_snapshot: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    cart: Mapped['Cart'] = relationship(back_populates='cartitem')
    product: Mapped['Product'] = relationship(Product)