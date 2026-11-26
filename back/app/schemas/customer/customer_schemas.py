from __future__ import annotations

from pydantic import BaseModel, EmailStr
from .cart_schemas import CartResponse
from typing import List
from .orders_chemas import OrderResponse


class CustomerBase(BaseModel):
    name: str
    email: EmailStr


class CustomerCreate(CustomerBase):
    password: str


class CustomerLogin(BaseModel):
    email: EmailStr
    password: str


class CustromerResponse(CustomerBase):
    id: int

    cart: CartResponse

    orders: List[OrderResponse]


class ChangePassword(BaseModel):
    old_password: str
    new_password: str