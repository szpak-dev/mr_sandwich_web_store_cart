from abc import ABC, abstractmethod

from shared.logger import logging

from product.domain.entities import Product
from product.domain.erorrs import ProductMustNotExist, ProductNotFound, ProductMustExist, DishCouldNotBeFound
from product.domain.event_listeners import FoodFactoryDishListener
from product.domain.models import FoodFactoryDish
from product.domain.repositories import FoodFactoryDishRepository, ProductRepository


def _update_product_properties(product: Product, dish: FoodFactoryDish) -> Product:
    product.dish_id = dish.id
    product.name = dish.name
    product.description = dish.description
    product.price = 1.22
    product.calories_per_100g = 123
    product.calories_per_serving = 444
    product.ingredients = dish.ingredients_text
    product.weight = 400
    return product


class ProductExistenceConstraints:
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository

    async def product_exists(self, dish_id: int) -> bool:
        try:
            await self._product_repository.get_by_dish_id(dish_id)
            return True
        except ProductNotFound:
            return False

    async def product_must_exist(self, dish_id: int) -> Product:
        """
        Raises:
            ProductMustExist: when Product does not exist
        """
        if not await self.product_exists(dish_id):
            raise ProductMustExist

        return await self._product_repository.get_by_dish_id(dish_id)

    async def product_must_not_exist(self, dish_id: int) -> None:
        """
        Raises:
            ProductMustNotExist: when Product exists
        """
        if await self.product_exists(dish_id):
            raise ProductMustNotExist


class ProductSaver:
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository

    async def save(self, product: Product) -> None:
        await self._product_repository.save(product)

    async def remove(self, product: Product) -> None:
        ...


class DishProvider:
    def __init__(self, dish_repository: FoodFactoryDishRepository):
        self._dish_repository = dish_repository

    async def get(self, dish_id: int) -> FoodFactoryDish:
        return await (anext(self._dish_repository.get_by_dish_id(dish_id)))


class DishChangeHandlingStrategy(ABC):
    @abstractmethod
    async def execute(self, dish: FoodFactoryDish) -> Product:
        ...


class DishCreated(DishChangeHandlingStrategy):
    def __init__(self, constraints: ProductExistenceConstraints):
        self._constraints = constraints

    async def execute(self, dish: FoodFactoryDish) -> Product:
        await self._constraints.product_must_not_exist(dish.id)
        return _update_product_properties(Product(), dish)


class DishUpdated(DishChangeHandlingStrategy):
    def __init__(self, constraints: ProductExistenceConstraints):
        self._constraints = constraints

    async def execute(self, dish: FoodFactoryDish) -> Product:
        product = await self._constraints.product_must_exist(dish.id)
        return _update_product_properties(product, dish)


class DishRemoved(DishChangeHandlingStrategy):
    def __init__(self, constraints: ProductExistenceConstraints):
        self._constraints = constraints

    async def execute(self, dish: FoodFactoryDish) -> Product:
        product = await self._constraints.product_must_exist(dish.id)
        return product


class DishChangeHandlingStrategyFactory:
    def __init__(self, constraints: ProductExistenceConstraints):
        self._constraints = constraints

    def create(self, operation_type: str) -> DishChangeHandlingStrategy:
        match operation_type:
            case 'dish_created':
                return DishCreated(self._constraints)
            case 'dish_updated':
                return DishUpdated(self._constraints)
            case 'dish_removed':
                return DishRemoved(self._constraints)


class AmqpFoodFactoryDishListener(FoodFactoryDishListener):
    def __init__(self, dish_repository: FoodFactoryDishRepository, product_repository: ProductRepository):
        self._dishes = DishProvider(dish_repository)
        self._constraints = ProductExistenceConstraints(product_repository)
        self._strategy_factory = DishChangeHandlingStrategyFactory(self._constraints)
        self._product_saver = ProductSaver(product_repository)

    async def on_dish_created(self, dish_id: int) -> None:
        try:
            dish = await self._dishes.get(dish_id)
            product = await self._strategy_factory.create('dish_created').execute(dish)
        except DishCouldNotBeFound:
            logging.error(f'Dish with id {dish_id} could not be found in Food Factory')
        except ProductMustNotExist:
            logging.warning(f'Product for Dish: {dish_id} already exists, updating properties')
            product = await self._strategy_factory.create('dish_created').execute(dish)

        await self._product_saver.save(product)

    async def on_dish_updated(self, dish_id: int) -> None:
        try:
            dish = await self._dishes.get(dish_id)
            product = await self._strategy_factory.create('dish_updated').execute(dish)
            await self._product_saver.save(product)
        except DishCouldNotBeFound:
            logging.error(f'Dish with id {dish_id} could not be found in Food Factory')
        except ProductMustExist:
            logging.warning(f'Product for Dish: {dish_id} does not exist, trying create strategy')
            await self._strategy_factory.create('dish_created').execute(dish)

    async def on_dish_removed(self, dish_id: int) -> None:
        try:
            dish = await self._dishes.get(dish_id)
            product = await self._strategy_factory.create('dish_removed').execute(dish)
        except DishCouldNotBeFound:
            logging.error(f'Dish with id {dish_id} could not be found in Food Factory')
        except ProductMustExist:
            logging.error(f'Product for removed Dish: {dish_id} does not exist, skipping')

        await self._product_saver.remove(product)
