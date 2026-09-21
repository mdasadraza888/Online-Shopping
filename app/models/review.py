from typing import TYPE_CHECKING, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from sqlalchemy import ForeignKey, Numeric, Case, DateTime, func
from decimal import Decimal
from datetime import datetime
from .user import User

if TYPE_CHECKING:
    from .product import Product

class Review(Base):
    __tablename__ = 'review'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    rating: Mapped[int] = mapped_column(Case())
    comment: Mapped[Text] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    product: Mapped['Product'] = relationship(back_populates='review')
    user: Mapped[User] = relationship(back_populates='review')