from dataclasses import dataclass

from command_coach.query import Query

from product.domain.entities import Product
from product.domain.value_objects import ProductId
from product.infrastructure import product_repository


@dataclass(frozen=True)
class GetProductQuery(Query):
    product_id: int

    def get_product_id(self) -> ProductId:
        return ProductId(self.product_id)


class GetProductQueryHandler:
    async def handle(self, query: GetProductQuery) -> Product:
        return await product_repository.get_by_id(query.get_product_id())
