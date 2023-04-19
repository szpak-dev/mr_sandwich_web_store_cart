from __future__ import annotations

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from shared.logger import logging
from cart.ui.http import controllers as cart_controllers
from product.ui.http import controllers as product_controllers
from cart.ui.http.responses import Cart
from product.ui.http.responses import Product, ProductListItem
from cart.ui.http.requests import AddProductToCart

app = FastAPI(
    root_path='/web_store_cart'
)


@app.on_event('startup')
async def on_startup():
    logging.info('Starting web_store_cart application')
    Instrumentator().instrument(app).expose(app, endpoint='/web_store_cart/metrics')


@app.get('/web_store_cart/carts', status_code=200, response_model=Cart, tags=['Cart'])
async def get_active_cart(customer_id: int) -> Cart:
    return await cart_controllers.get_active_cart(customer_id)


@app.post('/web_store_cart/carts', status_code=201, tags=['Cart'])
async def create_cart(customer_id: int):
    await cart_controllers.create_cart(customer_id)


@app.post('/web_store_cart/carts/{cart_id}/cart_products', status_code=201, tags=['Cart'])
async def add_product_to_cart(cart_id: int, product: AddProductToCart, customer_id: int):
    await cart_controllers.add_product_to_cart(cart_id, customer_id, product.product_id)


@app.delete('/web_store_cart/carts/{cart_id}/cart_products/{cart_product_id}', status_code=204, tags=['Cart'])
async def remove_product_from_cart(cart_id: int, cart_product_id: int, customer_id: int):
    await cart_controllers.remove_product_from_cart(cart_id, customer_id, cart_product_id)


@app.delete('/web_store_cart/carts/{cart_id}', status_code=204, tags=['Cart'])
async def clear_cart(cart_id: int, customer_id: int):
    await cart_controllers.clear_cart(cart_id, customer_id)


@app.get('/web_store_cart/products', status_code=200, response_model=list[ProductListItem], tags=['Product'])
async def get_products_list():
    p = await product_controllers.get_all_products()
    print(p[0])
    return p


@app.get('/web_store_cart/products/{product_id}', status_code=200, response_model=Product, tags=['Product'])
async def get_product(product_id: int):
    return await product_controllers.get_product(product_id)
