from httpx import AsyncClient, codes

from product.domain.erorrs import DishCouldNotBeFound
from product.domain.models import FoodFactoryDish
from product.domain.repositories import FoodFactoryDishRepository
from shared.config import settings


class HttpFoodFactoryDishRepository(FoodFactoryDishRepository):
    async def get_by_dish_id(self, dish_id: int) -> FoodFactoryDish:
        url = '{}/{}/{}'.format(settings['FOOD_FACTORY_URL'], 'food_factory/dishes', dish_id)
        async with AsyncClient() as client:
            response = await client.get(url)

            if response.status_code != codes.OK:
                raise DishCouldNotBeFound

            yield FoodFactoryDish(**response.json())
