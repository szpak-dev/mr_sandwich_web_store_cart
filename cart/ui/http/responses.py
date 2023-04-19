from typing import List
from pydantic import BaseModel


class CartProduct(BaseModel):
    id: int
    product_name: str
    price: float

    class Config:
        orm_mode = True


class Cart(BaseModel):
    id: int
    status: str
    total_price: float
    cart_products: List[CartProduct] = []

    class Config:
        orm_mode = True
