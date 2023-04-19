from shared.ddd import DomainEvent


class CartCreated(DomainEvent):
    def __init__(self):
        super().__init__('web_store_cart.cart.cart_created')

    def serialize(self) -> str:
        pass


class CartCleared(DomainEvent):
    def __init__(self):
        super().__init__('web_store_cart.cart.cart_cleared')

    def serialize(self) -> str:
        pass


class ProductAddedToCart(DomainEvent):
    def __init__(self):
        super().__init__('web_store_cart.cart.product_added_to_cart')

    def serialize(self) -> str:
        pass


class ProductRemovedFromCart(DomainEvent):
    def __init__(self):
        super().__init__('web_store_cart.cart.product_removed_from_cart')

    def serialize(self) -> str:
        pass
