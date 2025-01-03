from uuid import UUID
from typing import List, MutableSequence

from fastapi import Depends

from ... import app, manager
from ...config import URLPathsConfig
from ..services.category import (
    get_category, create_category, get_all_categories,
    update_category, delete_category
)
from ..schemas.category import (
    Category, CategoryCreate, CategoryUpdate
)


@app.post(
    URLPathsConfig.PREFIX + "/categories",
    tags=['Categories'],
    response_model=Category
)
async def create_category_route(
    item_in: CategoryCreate, user=Depends(manager)
) -> str:
    """
    Create new category.
    """
    category = await create_category(
        category_data=item_in
    )
    return category


@app.get(
    URLPathsConfig.PREFIX + "/categories",
    tags=['Categories'],
    response_model=List[Category]
)
async def get_all_categorys_route(user=Depends(manager)):
    categorys: MutableSequence[
        Category
    ] = await get_all_categories()
    return categorys


@app.get(
    URLPathsConfig.PREFIX + "/categories/{id}",
    tags=['Categories'],
    response_model=Category
)
async def get_category_route(id: UUID, user=Depends(manager)):
    category: Category = await get_category(id=id)
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
    result: Category = await delete_category(
        id=id
    )
    return result
