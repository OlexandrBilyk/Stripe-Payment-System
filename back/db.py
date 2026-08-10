from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import Enum as SQLEnum, ForeignKey
from typing import List
from enum import Enum
import os


class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELED = "canceled"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    REQUIRES_PAYMENT_METHOD = "requires_payment_method"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"
    REFUNDED = "refunded"


load_dotenv()

DB_URL = os.getenv('DB_URL')


Base = declarative_base()

engine = create_async_engine(DB_URL)

AsyncSessionLocal = async_sessionmaker(engine)


class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()

    orders: Mapped[List['Order']] = relationship(back_populates='customer')


class Order(Base):
    __tablename__ = 'orders'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus),
        default=OrderStatus.PENDING,
    )

    customer: Mapped['Customer'] = relationship(back_populates='orders')
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'))

    payments: Mapped[List['Payment']] = relationship(back_populates='order')


class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True)
    stripe_id: Mapped[str] = mapped_column(unique=True)
    status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus),
        default=PaymentStatus.PENDING,
    )

    order: Mapped['Order'] = relationship(back_populates='payments')
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column(default=0)


async def get_db():
    async with AsyncSessionLocal() as db:
        async with db.begin():
            yield db