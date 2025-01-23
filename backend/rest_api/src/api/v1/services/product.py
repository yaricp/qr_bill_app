from uuid import UUID
from typing import List

from ....app.product import ProductQueries, ProductCommands

from ..schemas.product import (
    Product, ProductCreate, ProductUpdate
)


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# -----Views-----


async def get_all_products() -> List[Product]:
    queries: ProductQueries = ProductQueries()
    return await queries.get_all_products()


async def get_product(id: UUID) -> Product:
    queries: ProductQueries = ProductQueries()
    return await queries.get_product(id=id)


# ------Actons(Commands)-------


async def create_product(
    product_data: ProductCreate
) -> Product:
    command = ProductCommands()
    command_result = await command.create_product(product_data)
    return command_result


async def update_product(
    id: UUID, product_data: ProductUpdate
) -> Product:

    command = ProductCommands()
    command_result = await command.update_product(
        product_data
    )
    return command_result


async def delete_product(id: UUID) -> Product:
    command = ProductCommands()
    command_result = await command.delete_product(id=id)
    return command_result
