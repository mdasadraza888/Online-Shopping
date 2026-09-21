from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from enum import Enum
from sqlalchemy import DateTime, func, Enum as SQLENUM
from app.core.database import Base

if TYPE_CHECKING:
    from .address import Address
    from .order import Order
    from .review import Review
    from .wishlist import Wishlist
    from .cart import Cart

class RoleType(str, Enum):
    SUPER_ADMIN = "super_admin"
    MANAGER = "manager"
    CATALOG_MANAGER = "catalog_manager"
    SUPPORT = "support"
    WAREHOUSE = "warehouse"
    CUSTOMER = "customer"
    VENDOR = "vendor"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str | None] = mapped_column(unique=True)
    role: Mapped[RoleType] = mapped_column(SQLENUM(RoleType, values_collable=lambda x: [e.value for e in x]), default=RoleType.CUSTOMER, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    addresses: Mapped[list['Address']]= relationship(back_populates="user", cascade="all, delete-orphan")
    orders: Mapped[list['Order']] = relationship(Order)
    reviews: Mapped[list['Review']] = relationship(back_populates='user')
    wishlist: Mapped[list['Wishlist']] = relationship(back_populates='user', cascade="all, delete-orphan")
    cart: Mapped['Cart'] = relationship(back_populates='user', uselist=False, cascade="all, delete-orphan")
