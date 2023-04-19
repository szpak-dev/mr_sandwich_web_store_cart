from dataclasses import dataclass

from command_coach.command import Command, CommandHandler

from cart.domain.value_objects import CustomerId
from cart.infrastructure import cart_repository


@dataclass(frozen=True)
class ClearCartCommand(Command):
    cart_id: int
    customer_id: int


class ClearCartCommandHandler(CommandHandler):
    async def handle(self, command: ClearCartCommand) -> None:
        customer_id = CustomerId(command.customer_id)
        cart = await cart_repository.get_active_for_customer(customer_id)
        cart.clear()
        await cart_repository.save(cart)
