from typing import List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select

from product.domain.entities import Product
from product.domain.erorrs import ProductNotFound
from product.domain.repositories import ProductRepository
from product.domain.value_objects import ProductId
from shared.db import Database


class SqlProductRepository(ProductRepository):
    def __init__(self, database: Database):
        self.session = database.current_session()

    async def get_by_id(self, product_id: ProductId) -> Product:
        try:
            result = await self.session.execute(
                select(Product)
                .filter(Product.id == product_id.id)
            )

            return result.scalars().one()
        except NoResultFound:
            raise ProductNotFound

    async def get_by_dish_id(self, dish_id: int) -> Product:
        try:
            result = await self.session.execute(
                select(Product)
                .filter(Product.dish_id == dish_id)
            )

            return result.scalars().one()
        except NoResultFound:
            raise ProductNotFound

    async def get_all(self) -> List[Product]:
        try:
            result = await self.session.execute(select(Product))
            return result.scalars().all()
        except NoResultFound:
            raise ProductNotFound

    async def save(self, product: Product) -> None:
        self.session.add(product)
