from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from .product import Product

class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(unique=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=True)

    product: Mapped['Product'] = relationship(back_populates='category')