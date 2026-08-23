from pydantic import BaseModel, field_validator
from .orders_chemas import BaseResponse
from typing import List
from .base_schemas import ProductResponse, BaseResponse


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, value: int):
        if value < 1:
            raise ValueError("Quantity must be at least 1")

        return value


class CartItemResponse(BaseResponse):
    id: int
    quantity: int
    product: ProductResponse


class CartResponse(BaseResponse):
    id: int
    cart_items: List[CartItemResponse]
