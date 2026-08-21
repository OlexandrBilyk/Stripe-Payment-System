from pydantic import BaseModel, EmailStr
from .cart_schemas import CartResponse
from typing import List


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

    # orders: List[]