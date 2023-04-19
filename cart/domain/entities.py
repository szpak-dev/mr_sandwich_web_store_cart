from datetime import datetime
from functools import reduce

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from cart.domain.erorrs import ProductNotInCart
from cart.domain.events import ProductAddedToCart, ProductRemovedFromCart, CartCleared
from cart.domain.value_objects import CartProductId, CustomerId
from shared.db_orm import Base
from shared.ddd import AggregateRoot
from shared.shared import Money


class Cart(Base, AggregateRoot):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    cart_products = relationship('CartProduct', lazy='joined', cascade='all, delete-orphan')
    customer_id = Column(Integer)
    reservation_id = Column(String, nullable=False)
    status = Column(String)
    total_price = Column(Float)
    created_at = Column(DateTime, default=datetime.now)

    def add_product(self, product_id: int, name: str, price: Money) -> None:
        self.cart_products.append(CartProduct(
            cart_id=self.id,
            product_id=product_id,
            product_name=name,
            price=price.value,
        ))

        self._recalculate()
        self._emit_event(ProductAddedToCart())

    def remove_product(self, cart_product_id: CartProductId):
        for cart_product in self.cart_products:
            if cart_product.id == cart_product_id.id:
                self.cart_products.remove(cart_product)
                self._recalculate()
                self._emit_event(ProductRemovedFromCart())
                return

        raise ProductNotInCart

    def clear(self):
        self.cart_products = []
        self._recalculate()
        self._emit_event(CartCleared())

    def _recalculate(self):
        if len(self.cart_products) == 0:
            self.total_price = 0
            return

        prices = [x.price for x in self.cart_products]
        self.total_price = reduce(lambda x, y: x + y, prices)


class CartProduct(Base):
    __tablename__ = 'cart_products'
    id = Column(Integer, primary_key=True)
    cart_id = Column(ForeignKey('carts.id'))
    product_id = Column(Integer)
    product_name = Column(String)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now)


def create_empty_cart(customer_id: CustomerId) -> Cart:
    cart = Cart()
    cart.customer_id = customer_id.id
    cart.status = 'ACTIVE'
    cart.total_price = 0.0
    return cart
