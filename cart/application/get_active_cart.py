from dataclasses import dataclass

from command_coach.query import Query

from cart.domain.entities import Cart
from cart.domain.value_objects import CustomerId
from cart.infrastructure import cart_repository


@dataclass(frozen=True)
class GetActiveCartQuery(Query):
    customer_id: int

    def get_customer_id(self) -> CustomerId:
        return CustomerId(self.customer_id)


class GetActiveCartQueryHandler:
    async def handle(self, query: GetActiveCartQuery) -> Cart:
        return await cart_repository.get_active_for_customer(query.get_customer_id())
