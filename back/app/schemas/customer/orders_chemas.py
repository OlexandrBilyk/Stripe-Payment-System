from typing import List
from app.models import OrderStatus, PaymentStatus
from .base_schemas import ProductResponse, BaseResponse


class OrderItemResponse(BaseResponse):
    id: int
    order_id: int
    product: ProductResponse
    quantity: int
    price: int


class PaymentResponse(BaseResponse):
    id: int
    stripe_id: str
    status: PaymentStatus
    order_id: int


class OrderResponse(BaseResponse):
    id: int
    status: OrderStatus
    payments: List[PaymentResponse]
    order_items: List[OrderItemResponse]