from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select

from cart.domain.entities import Cart, CartProduct
from cart.domain.erorrs import CartNotFound
from cart.domain.repository import CartRepository
from cart.domain.value_objects import CustomerId
from shared.db import Database


class SqlCartRepository(CartRepository):
    def __init__(self, database: Database):
        self.session = database.current_session()

    async def get_active_for_customer(self, customer_id: CustomerId) -> Cart:
        try:
            result = await self.session.execute(
                select(Cart)
                .filter(
                    Cart.customer_id == customer_id.id,
                    Cart.status == 'ACTIVE',
                )
                .join(CartProduct, isouter=True)
            )

            return result.unique().scalars().one()
        except NoResultFound:
            raise CartNotFound

    async def save(self, cart: Cart) -> None:
        self.session.add(cart)
