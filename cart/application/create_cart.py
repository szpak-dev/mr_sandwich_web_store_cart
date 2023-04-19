from dataclasses import dataclass

from command_coach.command import Command, CommandHandler

from cart.domain.entities import create_empty_cart
from cart.domain.erorrs import ActiveCartExists, CartNotFound
from cart.domain.value_objects import CustomerId
from cart.infrastructure import cart_repository


@dataclass(frozen=True)
class CreateCartCommand(Command):
    customer_id: int


class CreateCartCommandHandler(CommandHandler):
    async def handle(self, command: CreateCartCommand) -> None:
        customer_id = CustomerId(command.customer_id)
        try:
            await cart_repository.get_active_for_customer(customer_id)
            raise ActiveCartExists
        except CartNotFound:
            pass

        new_cart = create_empty_cart(customer_id)
        await cart_repository.save(new_cart)
