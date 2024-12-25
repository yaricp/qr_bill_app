from uuid import UUID
from typing import List

from ....app.category import (
    CategoryViews, CategoryQueries, CategoryCommands
)

from ..schemas.category import (
    Category, CategoryCreate, CategoryUpdate
)


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# ----Views----


async def get_all_categories() -> List[Category]:
    cat_views = CategoryViews()
    return await cat_views.get_all_categories()


async def get_category(id: UUID) -> Category:
    cat_query = CategoryQueries()
    return await cat_query.get_attraction(attraction_id=id)


# -----Actions-----


async def create_category(category_data: CategoryCreate) -> Category:
    cat_command = CategoryCommands()
    command_result = await cat_command.create_attraction(
        category_data
    )
    return command_result


async def update_category(category_data: CategoryUpdate) -> Category:
    cat_command = CategoryCommands()
    command_result = await cat_command.update_attraction(
        category_data
    )
    return command_result


async def delete_category(id: UUID) -> Category:
    cat_command = CategoryCommands()
    command_result = await cat_command.delete_attraction(id=id)
    return command_result
