from fastapi import HTTPException

from cart.domain.erorrs import CartNotFound, ActiveCartExists, ProductNotInCart
from shared.command_bus import bus, query_bus
from cart.application.add_product_to_cart import AddProductToCartCommand
from cart.application.clear_cart import ClearCartCommand
from cart.application.create_cart import CreateCartCommand
from cart.application.remove_product_from_cart import RemoveProductFromCartCommand
from cart.application.get_active_cart import GetActiveCartQuery
from cart.ui.http.responses import Cart


async def get_active_cart(customer_id: int) -> Cart:
    try:
        return await query_bus.handle(GetActiveCartQuery(customer_id))
    except CartNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


async def create_cart(customer_id: int) -> None:
    try:
        await bus.handle(CreateCartCommand(customer_id))
    except ActiveCartExists as e:
        raise HTTPException(status_code=409, detail=str(e))


async def add_product_to_cart(cart_id: int, customer_id: int, product_id: int) -> None:
    try:
        await bus.handle(AddProductToCartCommand(
            cart_id,
            customer_id,
            product_id,
        ))
    except CartNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


async def remove_product_from_cart(cart_id: int, customer_id: int, cart_product_id: int) -> None:
    try:
        await bus.handle(RemoveProductFromCartCommand(
            cart_id,
            customer_id,
            cart_product_id,
        ))
    except (CartNotFound, ProductNotInCart) as e:
        raise HTTPException(status_code=404, detail=str(e))


async def clear_cart(cart_id: int, customer_id: int) -> None:
    try:
        await bus.handle(ClearCartCommand(
            cart_id,
            customer_id,
        ))
    except CartNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
