from uuid import UUID
from typing import List

from ....app.category import (
    CategoryQueries, CategoryCommands
)

from ..schemas.category import (
    Category, CategoryCreate, CategoryUpdate,
    CategoryCountByName, CategorySummByName
)


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# ----Views----


async def get_all_categories(user_id: UUID) -> List[Category]:
    cat_views = CategoryQueries()
    return await cat_views.get_all_categories(user_id=user_id)


async def get_category(id: UUID, user_id: UUID) -> Category:
    cat_query = CategoryQueries()
    return await cat_query.get_category(
        id=id, user_id=user_id
    )


async def count_goods_by_name_categories(
    first_of: int, user_id: UUID, delta_month: int = 1
) -> CategoryCountByName:
    cat_query = CategoryQueries()
    return await cat_query.count_goods_by_name(
        first_of=first_of, user_id=user_id, delta_month=delta_month
    )


async def summ_goods_by_name_categories(
    first_of: int, user_id: UUID, delta_month: int = 1
) -> CategorySummByName:
    cat_query = CategoryQueries()
    return await cat_query.summ_goods_by_name(
        first_of=first_of, user_id=user_id, delta_month=delta_month
    )


# -----Actions-----


async def create_category(category_data: CategoryCreate) -> Category:
    cat_command = CategoryCommands()
    command_result = await cat_command.create_category(
        category_data
    )
    return command_result


async def update_category(category_data: CategoryUpdate) -> Category:
    cat_command = CategoryCommands()
    command_result = await cat_command.update_category(
        incoming_item=category_data
    )
    return command_result


async def delete_category(id: UUID) -> Category:
    cat_command = CategoryCommands()
    command_result = await cat_command.delete_category(id=id)
    return command_result
