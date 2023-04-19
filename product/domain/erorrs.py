from shared.ddd import DomainError
from shared.shared import docstring_message


@docstring_message
class ProductError(DomainError):
    """Product error"""


@docstring_message
class ProductNotFound(ProductError):
    """Product not found"""


@docstring_message
class ProductMustNotExist(ProductError):
    """Product with given dish_id already exists"""


@docstring_message
class ProductMustExist(ProductError):
    """Product with given dish_id does not exist"""


@docstring_message
class DishCouldNotBeFound(ProductError):
    """Dish does not exist in Food Factory"""
