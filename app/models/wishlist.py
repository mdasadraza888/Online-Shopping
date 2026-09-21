from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import DateTime, func
from app.core.database import Base
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .product import Product

class Wishlist(Base):
    __tablename__ = 'wishlists'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    user: Mapped['User'] = relationship(back_populates='wishlist')
    product: Mapped['Product'] = relationship(Product)