from dataclasses import dataclass
from typing import List

from command_coach.query import Query

from product.domain.entities import Product
from product.infrastructure import product_repository


@dataclass(frozen=True)
class GetAllProductsQuery(Query):
    ...


class GetAllProductsQueryHandler:
    async def handle(self, query: GetAllProductsQuery) -> List[Product]:
        return await product_repository.get_all()
