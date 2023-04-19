from abc import ABC, abstractmethod
from typing import List

from product.domain.entities import Product
from product.domain.models import FoodFactoryDish
from product.domain.value_objects import ProductId


class ProductRepository(ABC):
    @abstractmethod
    async def get_by_id(self, product_id: ProductId) -> Product:
        ...

    @abstractmethod
    async def get_by_dish_id(self, dish_id: int) -> Product:
        ...

    @abstractmethod
    async def get_all(self) -> List[Product]:
        ...

    @abstractmethod
    async def save(self, product: Product) -> None:
        ...


class FoodFactoryDishRepository(ABC):
    @abstractmethod
    async def get_by_dish_id(self, dish_id: int) -> FoodFactoryDish:
        ...
