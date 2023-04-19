from abc import ABC, abstractmethod

from cart.domain.entities import Cart
from cart.domain.value_objects import CustomerId


class CartRepository(ABC):
    @abstractmethod
    async def get_active_for_customer(self, customer_id: CustomerId) -> Cart:
        pass

    @abstractmethod
    async def save(self, cart: Cart) -> None:
        pass
