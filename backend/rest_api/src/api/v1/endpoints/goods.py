from uuid import UUID
from typing import List, MutableSequence

from fastapi import Depends
from loguru import logger

from ... import app, manager
from ...config import URLPathsConfig
from ..services.goods import (
    get_goods, create_goods, get_all_goods,
    update_goods, delete_goods, list_count_group_by_name,
    list_summ_group_by_name, strip_all_names,
    list_uncategorized_goods, save_categorized_goods,
    update_goods_categories
)
from ..schemas.goods import (
    Goods, GoodsCreate, GoodsUpdate, GoodsCountByName,
    GoodsSummByName, CategoryGoods
)


@app.post(
    URLPathsConfig.PREFIX + "/goods",
    tags=['Goods'],
    response_model=Goods
)
async def create_goods_route(
    item_in: GoodsCreate, user=Depends(manager)
) -> str:
    """
    Create new goods.
    """
    item_in.user_id = user.id
    goods = await create_goods(goods_data=item_in)
    return goods


@app.post(
    URLPathsConfig.PREFIX + "/goods/save_categorized/",
    tags=['Goods'],
    response_model=bool
)
async def save_categorized_goods_route(
    data_in: List[CategoryGoods], user=Depends(manager)
) -> bool:
    """
    Assosiate category to several goods.
    """
    result = await save_categorized_goods(
        goods_data=data_in
    )
    return result


@app.post(
    URLPathsConfig.PREFIX + "/goods/update_category/{goods_id}",
    tags=['Goods'],
    response_model=bool
)
async def update_categorized_goods_route(
    goods_id: UUID, data_in: List[CategoryGoods], user=Depends(manager)
) -> bool:
    """
    Update categories for one good.
    """
    result = await update_goods_categories(
        goods_id=goods_id, goods_data=data_in
    )
    return result


@app.get(
    URLPathsConfig.PREFIX + "/goods",
    tags=['Goods'],
    response_model=List[Goods]
)
async def get_all_goods_route(user=Depends(manager)):
    logger.info(f"user.id: {user.id}")
    goodss: MutableSequence[
        Goods
    ] = await get_all_goods(user_id=user.id)
    return goodss


@app.get(
    URLPathsConfig.PREFIX + "/goods/{id}",
    tags=['Goods'],
    response_model=Goods
)
async def get_goods_route(id: UUID, user=Depends(manager)):
    goods: Goods = await get_goods(id=id)
    return goods


@app.put(
    URLPathsConfig.PREFIX + "/goods/{id}",
    tags=['Goods'],
    response_model=Goods
)
async def put_goods_route(
    id: UUID, item_in: GoodsUpdate, user=Depends(manager)
):
    item_in.id = id
    item_in.user_id = user.id
    goods: Goods = await update_goods(goods_data=item_in)
    return goods


@app.delete(
    URLPathsConfig.PREFIX + "/goods/{id}",
    tags=['Goods'],
    response_model=Goods
)
async def delete_goods_route(id: UUID, user=Depends(manager)):
    result: Goods = await delete_goods(
        id=id, user_id=user.id
    )
    return result


@app.get(
    URLPathsConfig.PREFIX + "/goods/uncategorized/{cat_id}",
    tags=['Goods'],
    response_model=List[Goods]
)
async def uncategorized_goods_cat_route(
    cat_id: UUID, user=Depends(manager)
) -> List[Goods]:
    result: List[Goods] = await list_uncategorized_goods(
        user_id=user.id, cat_id=cat_id
    )
    return result


@app.get(
    URLPathsConfig.PREFIX + "/goods/uncategorized/",
    tags=['Goods'],
    response_model=List[Goods]
)
async def uncategorized_goods_route(
    user=Depends(manager)
) -> List[Goods]:
    result: List[Goods] = await list_uncategorized_goods(
        user_id=user.id
    )
    return result


@app.get(
    URLPathsConfig.PREFIX + "/goods/count_by_name/",
    tags=['Goods'],
    response_model=List[GoodsCountByName]
)
async def count_by_name_goods_route(
    first_of: int = 0, user=Depends(manager)
) -> List[GoodsCountByName]:
    logger.info(f"first_of: {first_of}")
    result: List[
        GoodsCountByName
    ] = await list_count_group_by_name(
        first_of=first_of, user_id=user.id
    )
    return result


@app.get(
    URLPathsConfig.PREFIX + "/goods/summ_by_name/",
    tags=['Goods'],
    response_model=List[GoodsSummByName]
)
async def summ_by_name_goods_route(
    first_of: int = 0, user=Depends(manager)
) -> List[GoodsSummByName]:
    result: List[
        GoodsSummByName
    ] = await list_summ_group_by_name(
        first_of=first_of, user_id=user.id
    )
    return result


@app.get(
    URLPathsConfig.PREFIX + "/goods/strip_all_names/",
    tags=['Goods'],
    response_model=bool
)
async def strip_all_names_goods_route(user=Depends(manager)) -> bool:
    result: bool = await strip_all_names()
    return result
