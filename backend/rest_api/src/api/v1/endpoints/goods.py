from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException
from loguru import logger

from ... import app, manager
from ...config import URLPathsConfig
from ..schemas.goods import (CategoryGoods, Goods, GoodsCountByName,
                             GoodsCreate, GoodsSummByName, GoodsUpdate)
from ..services.goods import (create_goods, delete_goods, get_all_goods,
                              get_goods, list_count_group_by_name,
                              list_summ_group_by_name,
                              list_uncategorized_goods, update_goods,
                              update_goods_categories)


@app.post(URLPathsConfig.PREFIX + "/goods/", tags=["Goods"], response_model=Goods)
async def create_goods_route(item_in: GoodsCreate, user=Depends(manager)) -> Goods:
    """Creates a new goods"""
    item_in.user_id = user.id
    goods = await create_goods(goods_data=item_in)
    return goods


@app.post(
    URLPathsConfig.PREFIX + "/goods/update_category/{goods_id}",
    tags=["Goods"],
    response_model=bool,
)
async def update_categorized_goods_route(
    goods_id: UUID, data_in: List[CategoryGoods], user=Depends(manager)
) -> bool:
    """Updates a categories for one goods"""
    result = await update_goods_categories(goods_id=goods_id, goods_data=data_in)
    return result


@app.get(URLPathsConfig.PREFIX + "/goods/", tags=["Goods"], response_model=List[Goods])
async def get_all_goods_route(
    offset: int = 0, limit: int = 0, user=Depends(manager)
) -> List[Goods]:
    """Shows list goods of current user"""
    logger.info(f"user.id: {user.id}")
    goodss: List[Goods] = await get_all_goods(
        user_id=user.id, offset=offset, limit=limit
    )
    return goodss


@app.get(URLPathsConfig.PREFIX + "/goods/{id}", tags=["Goods"], response_model=Goods)
async def get_goods_route(id: UUID, user=Depends(manager)) -> Goods:
    """Shows goods info"""
    goods: Goods = await get_goods(id=id)
    if not goods:
        raise HTTPException(status_code=404, detail="Goods not found")
    return goods


@app.put(URLPathsConfig.PREFIX + "/goods/{id}", tags=["Goods"], response_model=Goods)
async def put_goods_route(
    id: UUID, item_in: GoodsUpdate, user=Depends(manager)
) -> Goods:
    """Updates goods info"""
    item_in.id = id
    item_in.user_id = user.id
    goods: Goods = await update_goods(goods_data=item_in)
    if not goods:
        raise HTTPException(status_code=404, detail="Goods not found")
    return goods


@app.delete(URLPathsConfig.PREFIX + "/goods/{id}", tags=["Goods"], response_model=Goods)
async def delete_goods_route(id: UUID, user=Depends(manager)) -> Goods:
    """Deletes goods"""
    goods: Goods = await delete_goods(id=id, user_id=user.id)
    if not goods:
        raise HTTPException(status_code=404, detail="Goods not found")
    return goods


@app.get(
    URLPathsConfig.PREFIX + "/goods/uncategorized/{cat_id}",
    tags=["Goods"],
    response_model=List[Goods],
)
async def uncategorized_goods_cat_route(
    cat_id: UUID, user=Depends(manager)
) -> List[Goods]:
    """Shows a list of goods not assigned to a particular category"""
    result: List[Goods] = await list_uncategorized_goods(user_id=user.id, cat_id=cat_id)
    return result


@app.get(
    URLPathsConfig.PREFIX + "/goods/uncategorized/",
    tags=["Goods"],
    response_model=List[Goods],
)
async def uncategorized_goods_route(user=Depends(manager)) -> List[Goods]:
    """Shows a list of goods not assigned to any category"""
    result: List[Goods] = await list_uncategorized_goods(user_id=user.id)
    return result


@app.get(
    URLPathsConfig.PREFIX + "/goods/count_by_name/",
    tags=["Goods"],
    response_model=List[GoodsCountByName],
)
async def count_by_name_goods_route(
    first_of: int = 0, user=Depends(manager)
) -> List[GoodsCountByName]:
    """Shows analytics of goods quantities by name"""
    logger.info(f"first_of: {first_of}")
    result: List[GoodsCountByName] = await list_count_group_by_name(
        first_of=first_of, user_id=user.id
    )
    return result


@app.get(
    URLPathsConfig.PREFIX + "/goods/summ_by_name/",
    tags=["Goods"],
    response_model=List[GoodsSummByName],
)
async def summ_by_name_goods_route(
    first_of: int = 0, user=Depends(manager)
) -> List[GoodsSummByName]:
    """Shows analytics of goods costs by name"""
    result: List[GoodsSummByName] = await list_summ_group_by_name(
        first_of=first_of, user_id=user.id
    )
    return result
