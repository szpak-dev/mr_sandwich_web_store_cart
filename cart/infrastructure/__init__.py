from cart.domain.repository import CartRepository
from cart.infrastructure.sql_cart_repository import SqlCartRepository
from shared.db import database

cart_repository: CartRepository = SqlCartRepository(database)
