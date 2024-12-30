from uuid import UUID
from typing import List, MutableSequence

from fastapi import APIRouter, Depends
from loguru import logger


from ..services.goods import (
    get_goods, create_goods, get_all_goods,
    update_goods, delete_goods, list_count_group_by_name,
    list_summ_group_by_name, strip_all_names
)
from ..schemas.goods import (
    Goods, GoodsCreate, GoodsUpdate, GoodsCountByName,
    GoodsSummByName
)


router = APIRouter()


@router.post(
    "/", response_model=Goods
)
async def create_goods_route(
    *, item_in: GoodsCreate
) -> str:
    """
    Create new goods.
    """
    goods = await create_goods(
        goods_data=item_in
    )
    return goods


@router.get("/", response_model=List[Goods])
async def get_all_goods_route():
    goodss: MutableSequence[
        Goods
    ] = await get_all_goods()
    return goodss


@router.get("/{id}", response_model=Goods)
async def get_goods_route(id: UUID):
    goods: Goods = await get_goods(id=id)
    return goods


@router.put("/{id}", response_model=Goods)
async def put_goods_route(
    id: UUID, item_in: GoodsUpdate
):
    item_in.id = id
    goods: Goods = await update_goods(
        goods_data=item_in
    )
    return goods


@router.delete("/{id}", response_model=Goods)
async def delete_goods_route(id: UUID):
    result: Goods = await delete_goods(
        id=id
    )
    return result


@router.get("/count_by_name/", response_model=List[GoodsCountByName])
async def count_by_name_goods_route(first_of: int = 0) -> List[GoodsCountByName]:
    logger.info(f"first_of: {first_of}")
    result: List[
        GoodsCountByName
    ] = await list_count_group_by_name(first_of=first_of)
    return result


@router.get("/summ_by_name/", response_model=List[GoodsSummByName])
async def summ_by_name_goods_route(first_of: int = 0) -> List[GoodsSummByName]:
    result: List[
        GoodsSummByName
    ] = await list_summ_group_by_name(first_of=first_of)
    return result


@router.get("/strip_all_names/", response_model=bool)
async def strip_all_names_goods_route() -> bool:
    result: bool = await strip_all_names()
    return result
