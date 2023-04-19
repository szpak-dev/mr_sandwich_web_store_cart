from dataclasses import dataclass
from typing import List


@dataclass
class FoodFactoryDishIngredient:
    name: str
    calories: float


@dataclass
class FoodFactoryDish:
    id: int
    name: str
    description: str
    ingredients: List[FoodFactoryDishIngredient]

    @property
    def ingredients_text(self) -> str:
        return ', '.join([i['name'] for i in self.ingredients])
