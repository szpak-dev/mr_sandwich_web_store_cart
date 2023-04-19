from shared.ddd import DomainEvent


class ProductCreated(DomainEvent):
    def __init__(self):
        super().__init__('web_store_cart.product.product_created')

    def serialize(self) -> str:
        pass


class ProductUpdated(DomainEvent):
    def __init__(self):
        super().__init__('web_store_cart.product.updated')

    def serialize(self) -> str:
        pass


class ProductDeactivated(DomainEvent):
    def __init__(self):
        super().__init__('web_store_cart.product.product_deactivated')

    def serialize(self) -> str:
        pass
