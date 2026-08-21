from pydantic import BaseModel, field_validator
from typing import List

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, value: int):
        if value < 1:
            raise ValueError("Quantity must be at least 1")

        return value


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        from_attributes = True



class CartItemResponse(BaseModel):
    id: int
    quantity: int
    product: ProductResponse

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: int
    cart_items: List[CartItemResponse]

    class Config:
        from_attributes = True
