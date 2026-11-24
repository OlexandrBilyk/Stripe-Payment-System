from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Enum as SQLEnum, ForeignKey
from app.db import Base
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order


class PaymentStatus(str, Enum):
    REQUIRES_PAYMENT_METHOD = "requires_payment_method"
    REQUIRES_CONFIRMATION = "requires_confirmation"
    REQUIRES_ACTION = "requires_action"
    PROCESSING = "processing"
    REQUIRES_CAPTURE = "requires_capture"
    CANCELED = "canceled"
    SUCCEEDED = "succeeded"


class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True)
    stripe_id: Mapped[str] = mapped_column(unique=True)
    status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus),
        default=PaymentStatus.REQUIRES_PAYMENT_METHOD,
    )

    order: Mapped['Order'] = relationship(back_populates='payments')
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
