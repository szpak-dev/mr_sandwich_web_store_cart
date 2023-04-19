from pydantic import BaseModel


class AddProductToCart(BaseModel):
    product_id: int
