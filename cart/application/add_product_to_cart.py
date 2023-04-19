from dataclasses import dataclass
import random

from command_coach.command import Command, CommandHandler
from cart.domain.value_objects import CustomerId
from cart.infrastructure import cart_repository
from shared.shared import Money


@dataclass(frozen=True)
class AddProductToCartCommand(Command):
    cart_id: int
    customer_id: int
    product_id: int


class AddProductToCartCommandHandler(CommandHandler):
    async def handle(self, command: AddProductToCartCommand) -> None:
        customer_id = CustomerId(command.customer_id)
        cart = await cart_repository.get_active_for_customer(customer_id)

        cart.add_product(
            command.product_id,
            'Product name-{}'.format(random.random()),
            Money(random.randint(40, 200), 'USD'),
        )

        await cart_repository.save(cart)
