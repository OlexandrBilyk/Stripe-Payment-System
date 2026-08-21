from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from app.db import Base

if TYPE_CHECKING:
    from .cart import Cart
    from .product import Product


class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(primary_key=True)

    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'))
    cart: Mapped['Cart'] = relationship(back_populates='cart_items')

    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    product: Mapped['Product'] = relationship(back_populates='cart_items')

    quantity: Mapped[int] = mapped_column(default=1)