from dataclasses import dataclass

from command_coach.command import Command, CommandHandler

from product.infrastructure import food_factory_dish_listener


@dataclass(frozen=True)
class UpdateProductCommand(Command):
    dish_id: int
    operation_type: str


class UpdateProductCommandHandler(CommandHandler):
    async def handle(self, command: UpdateProductCommand):
        dish_id = command.dish_id

        match command.operation_type:
            case 'dish_created':
                await food_factory_dish_listener.on_dish_created(dish_id)
            case 'dish_updated':
                await food_factory_dish_listener.on_dish_updated(dish_id)
            case 'dish_removed':
                await food_factory_dish_listener.on_dish_removed(dish_id)
