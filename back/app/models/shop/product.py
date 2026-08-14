from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING, List
from app.db import Base

if TYPE_CHECKING:
    from .cart_items import CartItem


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column(default=0)

    cart_items: Mapped[List['CartItem']] = relationship(back_populates='product')
