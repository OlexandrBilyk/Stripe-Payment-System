from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from app.db import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..orders import Order
    from ..shop import Cart


class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=True)
    provider: Mapped[str] = mapped_column(nullable=True)
    provider_id: Mapped[str] = mapped_column(nullable=True)

    orders: Mapped[List['Order']] = relationship(back_populates='customer')
    cart: Mapped['Cart'] = relationship(back_populates='customer')
