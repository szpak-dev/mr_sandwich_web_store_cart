from typing import List

from fastapi import HTTPException

from product.application.get_all_products import GetAllProductsQuery
from product.application.get_product import GetProductQuery
from product.domain.erorrs import ProductNotFound
from shared.command_bus import query_bus
from product.domain.entities import Product


async def get_all_products() -> List[Product]:
    try:
        return await query_bus.handle(GetAllProductsQuery())
    except ProductNotFound:
        return []


async def get_product(product_id: int) -> Product:
    try:
        return await query_bus.handle(GetProductQuery(product_id))
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
