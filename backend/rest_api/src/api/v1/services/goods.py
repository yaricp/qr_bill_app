from uuid import UUID
from typing import List
from loguru import logger

from ....app.goods import GoodsQueries, GoodsCommands

from ..schemas.goods import (
    Goods, GoodsCreate, GoodsUpdate, GoodsCountByName,
    GoodsSummByName
)


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# -------Views---------


async def get_all_goods(user_id: UUID) -> List[Goods]:
    goods_views: GoodsQueries = GoodsQueries()
    return await goods_views.get_all_goods(user_id=user_id)


async def get_goods(id: UUID) -> Goods:
    goods_views: GoodsQueries = GoodsQueries()
    return await goods_views.get_goods(id=id)


async def list_count_group_by_name(
    first_of: int, user_id: UUID
) -> List[GoodsCountByName]:
    goods_queries: GoodsQueries = GoodsQueries()
    logger.info(f"first_of: {first_of}")
    result: List[
        GoodsCountByName
    ] = await goods_queries.list_count_group_by_name(
        first_of=first_of, user_id=user_id
    )
    return result


async def list_summ_group_by_name(
    first_of: int, user_id: UUID
) -> List[GoodsSummByName]:
    goods_queries: GoodsQueries = GoodsQueries()
    result: List[
        GoodsSummByName
    ] = await goods_queries.list_summ_group_by_name(
        first_of=first_of, user_id=user_id
    )
    return result


# --------Actions (commands) ---------


async def create_goods(
    goods_data: GoodsCreate
) -> Goods:
    goods_command = GoodsCommands()
    command_result = await goods_command.create_goods(
        goods_data
    )
    return command_result


async def update_goods(
    goods_data: GoodsUpdate
) -> Goods:
    goods_command = GoodsCommands()
    command_result = await goods_command.update_goods(
        incoming_item=goods_data
    )
    return command_result


async def delete_goods(id: UUID, user_id: UUID) -> Goods:
    goods_command = GoodsCommands()
    command_result = await goods_command.delete_goods(
        id=id, user_id=user_id
    )
    return command_result


async def strip_all_names() -> bool:
    goods_command = GoodsCommands()
    result: bool = await goods_command.strip_all_names()
    return result
