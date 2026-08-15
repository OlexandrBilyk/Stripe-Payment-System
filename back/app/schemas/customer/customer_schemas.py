from pydantic import BaseModel, EmailStr
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

    # orders: List[]