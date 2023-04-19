from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    price: float
    ingredients: str
    weight: float

    class Config:
        orm_mode = True


class ProductListItem(BaseModel):
    name: str
    price: float

    class Config:
        orm_mode = True
