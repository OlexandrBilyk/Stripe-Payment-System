from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Enum as SQLEnum, ForeignKey
from app.db import Base
from enum import Enum
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .payment import Payment
    from ..customer import Customer
    from ..shop import Product


class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELED = "canceled"


class Order(Base):
    __tablename__ = 'orders'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus),
        default=OrderStatus.PENDING,
    )

    customer: Mapped['Customer'] = relationship(back_populates='orders')
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'))

    payments: Mapped[List['Payment']] = relationship(back_populates='order')

    order_items: Mapped[List['OrderItem']] = relationship(back_populates='order')


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True)

    order: Mapped['Order'] = relationship(back_populates='order_items')
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))

    product: Mapped['Product'] = relationship(back_populates='order_items')
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))

    quantity: Mapped[int] = mapped_column()

    price: Mapped[int] = mapped_column()