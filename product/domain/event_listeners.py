from abc import ABC, abstractmethod


class FoodFactoryDishListener(ABC):
    @abstractmethod
    async def on_dish_created(self, dish_id: int) -> None:
        ...

    @abstractmethod
    async def on_dish_updated(self, dish_id: int) -> None:
        ...

    @abstractmethod
    async def on_dish_removed(self, dish_id: int) -> None:
        ...
