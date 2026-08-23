from pydantic import BaseModel

class BaseResponse(BaseModel):
    class Config:
        from_attributes = True


class ProductResponse(BaseResponse):
    id: int
    name: str
    price: int
