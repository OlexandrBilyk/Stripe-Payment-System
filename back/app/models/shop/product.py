from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING, List
from app.db import Base

if TYPE_CHECKING:
    from .cart import Cart


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column(default=0)

    carts: Mapped[List['Cart']] = relationship(back_populates='products')
