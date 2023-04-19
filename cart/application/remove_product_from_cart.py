from dataclasses import dataclass

from command_coach.command import Command, CommandHandler

from cart.domain.value_objects import CustomerId, CartProductId
from cart.infrastructure import cart_repository


@dataclass(frozen=True)
class RemoveProductFromCartCommand(Command):
    cart_id: int
    customer_id: int
    cart_product_id: int


class RemoveProductFromCartCommandHandler(CommandHandler):
    async def handle(self, command: RemoveProductFromCartCommand) -> None:
        customer_id = CustomerId(command.customer_id)
        cart_product_id = CartProductId(command.cart_product_id)

        cart = await cart_repository.get_active_for_customer(customer_id)
        cart.remove_product(cart_product_id)

        await cart_repository.save(cart)
