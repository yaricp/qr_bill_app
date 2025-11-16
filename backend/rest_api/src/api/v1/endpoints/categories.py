from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException

from ... import app, manager
from ...config import URLPathsConfig
from ..schemas.category import (Category, CategoryCountByName, CategoryCreate,
                                CategorySummByName, CategoryUpdate)
from ..services.category import (count_goods_by_name_categories,
                                 create_category, delete_category,
                                 get_all_categories, get_category,
                                 summ_goods_by_name_categories,
                                 update_category)


@app.post(
    URLPathsConfig.PREFIX + "/categories/", tags=["Categories"], response_model=Category
)
async def create_category_route(
    item_in: CategoryCreate, user=Depends(manager)
) -> Category:
    """Creates a new category"""
    item_in.user_id = user.id
    category = await create_category(category_data=item_in)
    return category


@app.get(
    URLPathsConfig.PREFIX + "/categories/",
    tags=["Categories"],
    response_model=List[Category],
)
async def get_all_categories_route(user=Depends(manager)) -> List[Category]:
    """Shows list of categories"""
    categories: List[Category] = await get_all_categories(user_id=user.id)
    return categories


@app.get(
    URLPathsConfig.PREFIX + "/categories/{id}",
    tags=["Categories"],
    response_model=Category,
)
async def get_category_route(id: UUID, user=Depends(manager)) -> Category:
    """Shows category info."""
    category: Category = await get_category(id=id, user_id=user.id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.put(
    URLPathsConfig.PREFIX + "/categories/{id}",
    tags=["Categories"],
    response_model=Category,
)
async def put_category_route(
    id: UUID, item_in: CategoryUpdate, user=Depends(manager)
) -> Category:
    """Updates a category"""
    item_in.id = id
    item_in.user_id = user.id
    category: Category = await update_category(category_data=item_in)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.delete(
    URLPathsConfig.PREFIX + "/categories/{id}",
    tags=["Categories"],
    response_model=Category,
)
async def delete_category_route(id: UUID, user=Depends(manager)) -> Category:
    """Deletes of a category"""
    category: Category = await delete_category(id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.get(
    URLPathsConfig.PREFIX + "/categories/count_goods_by_name/",
    tags=["Categories"],
    response_model=List[CategoryCountByName],
)
async def count_goods_by_name_route(
    first_of: int = 0, delta_month: int = 1, user=Depends(manager)
) -> List[CategoryCountByName]:
    """Shows analytics of goods counts by category names"""
    categories: List[CategoryCountByName] = await count_goods_by_name_categories(
        first_of=first_of, user_id=user.id, delta_month=delta_month
    )
    return categories


@app.get(
    URLPathsConfig.PREFIX + "/categories/summ_goods_by_name/",
    tags=["Categories"],
    response_model=List[CategorySummByName],
)
async def summ_goods_by_name_route(
    first_of: int = 0, delta_month: int = 1, user=Depends(manager)
) -> List[CategorySummByName]:
    """Shows analytics of goods costs by category names"""
    categories: List[CategorySummByName] = await summ_goods_by_name_categories(
        first_of=first_of, user_id=user.id, delta_month=delta_month
    )
    return categories
