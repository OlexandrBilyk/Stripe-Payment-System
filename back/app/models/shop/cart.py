from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List
from app.db import Base

if TYPE_CHECKING:
    from ..customer import Customer
    from .product import Product


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True)

    customer: Mapped['Customer'] = relationship(back_populates='cart')
    customer_id: Mapped[int] = relationship(ForeignKey('customers.id'))

    products: Mapped[List['Product']] = relationship(back_populates='carts')

