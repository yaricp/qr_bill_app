from uuid import UUID
from typing import List, MutableSequence

from fastapi import APIRouter, Depends
# from loguru import logger

from ..services.category import (
    get_category, create_category, get_all_categories,
    update_category, delete_category
)
from ..schemas.category import (
    Category, CategoryCreate, CategoryUpdate
)


router = APIRouter()


@router.post(
    "/", response_model=Category
)
async def create_category_route(
    *, item_in: CategoryCreate
) -> str:
    """
    Create new category.
    """
    category = await create_category(
        category_data=item_in
    )
    return category


@router.get("/", response_model=List[Category])
async def get_all_categorys_route():
    categorys: MutableSequence[
        Category
    ] = await get_all_categories()
    return categorys


@router.get("/{id}", response_model=Category)
async def get_category_route(id: UUID):
    category: Category = await get_category(id=id)
    return category


@router.put("/{id}", response_model=Category)
async def put_category_route(
    id: UUID, item_in: CategoryUpdate
):
    item_in.id = id
    category: Category = await update_category(
        category_data=item_in
    )
    return category


@router.delete("/{id}", response_model=Category)
async def delete_category_route(id: UUID):
    result: Category = await delete_category(
        id=id
    )
    return result
