from uuid import UUID
from typing import List
from loguru import logger

from ....app.product import ProductQueries, ProductCommands

from ..schemas.product import (
    Product, ProductCreate, ProductUpdate
)
from ..schemas.user_product import (
    UncategorizedUserProduct, CategorizedProduct
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


async def get_uncategorized_product(
    user_id: UUID, cat_id: UUID | None = None
) -> List[UncategorizedUserProduct]:
    queries: ProductQueries = ProductQueries()
    return await queries.get_uncategorized_product(
        user_id=user_id, cat_id=cat_id
    )


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


async def save_categorized_products(
    cat_prod_data: List[CategorizedProduct]
) -> bool:
    prod_command = ProductCommands()
    logger.info(f"cat_prod_data: {cat_prod_data}")
    command_result = await prod_command.save_categorized_products(
        cat_prod_data=cat_prod_data
    )
    return command_result


async def update_product_categories(
    user_product_id: UUID, list_cat_id: List[UUID]
) -> bool:
    prod_command = ProductCommands()
    logger.info(f"user_product_id: {user_product_id}")
    logger.info(f"list_cat_id: {list_cat_id}")
    command_result = await prod_command.update_product_categories(
        user_product_id=user_product_id, list_cat_id=list_cat_id
    )
    return command_result
