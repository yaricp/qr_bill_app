from uuid import UUID
from typing import List, MutableSequence

from fastapi import Depends

from ... import app, manager
from ...config import URLPathsConfig
from ..services.category import (
    get_category, get_all_categories,
    update_category, delete_category, create_category,
    count_goods_by_name_categories, summ_goods_by_name_categories
)
from ..schemas.category import (
    Category, CategoryCreate, CategoryUpdate,
    CategoryCountByName, CategorySummByName
)


@app.post(
    URLPathsConfig.PREFIX + "/categories/",
    tags=['Categories'],
    response_model=Category
)
async def create_category_route(
    item_in: CategoryCreate, user=Depends(manager)
) -> str:
    """
    Create new category.
    """
    item_in.user_id = user.id
    category = await create_category(
        category_data=item_in
    )
    return category


@app.get(
    URLPathsConfig.PREFIX + "/categories/",
    tags=['Categories'],
    response_model=List[Category]
)
async def get_all_categories_route(user=Depends(manager)):
    categories: List[
        Category
    ] = await get_all_categories(user_id=user.id)
    return categories


@app.get(
    URLPathsConfig.PREFIX + "/categories/{id}",
    tags=['Categories'],
    response_model=Category
)
async def get_category_route(id: UUID, user=Depends(manager)):
    category: Category = await get_category(id=id, user_id=user.id)
    return category


@app.put(
    URLPathsConfig.PREFIX + "/categories/{id}",
    tags=['Categories'],
    response_model=Category
)
async def put_category_route(
    id: UUID, item_in: CategoryUpdate, user=Depends(manager)
):
    item_in.id = id
    item_in.user_id = user.id
    category: Category = await update_category(
        category_data=item_in
    )
    return category


@app.delete(
    URLPathsConfig.PREFIX + "/categories/{id}",
    tags=['Categories'],
    response_model=Category
)
async def delete_category_route(id: UUID, user=Depends(manager)):
    result: Category = await delete_category(id=id)
    return result


@app.get(
    URLPathsConfig.PREFIX + "/categories/count_goods_by_name/",
    tags=['Categories'],
    response_model=List[CategoryCountByName]
)
async def count_goods_by_name_route(
    first_of: int = 0, delta_month: int = 1, user=Depends(manager)
) -> List[CategoryCountByName]:
    categories: List[
        CategoryCountByName
    ] = await count_goods_by_name_categories(
        first_of=first_of, user_id=user.id, delta_month=delta_month
    )
    return categories


@app.get(
    URLPathsConfig.PREFIX + "/categories/summ_goods_by_name/",
    tags=['Categories'],
    response_model=List[CategorySummByName]
)
async def summ_goods_by_name_route(
    first_of: int = 0, delta_month: int = 1, user=Depends(manager)
) -> List[CategorySummByName]:
    categories: List[
        CategorySummByName
    ] = await summ_goods_by_name_categories(
        first_of=first_of, user_id=user.id, delta_month=delta_month
    )
    return categories
