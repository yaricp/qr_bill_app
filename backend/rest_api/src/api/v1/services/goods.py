from uuid import UUID
from typing import List

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


async def get_all_goods() -> List[Goods]:
    goods_views: GoodsQueries = GoodsQueries()
    return await goods_views.get_all_goods()


async def get_goods(id: UUID) -> Goods:
    goods_views: GoodsQueries = GoodsQueries()
    return await goods_views.get_goods(id=id)


# --------Actions (commands) ---------


async def create_goods(
    goods_data: GoodsCreate
) -> Goods:
    goods_command = GoodsCommands()
    command_result = await goods_command.create_goods(
        **goods_data.model_dump()
    )
    return command_result


async def update_goods(
    goods_data: GoodsUpdate
) -> Goods:
    goods_command = GoodsCommands()
    command_result = await goods_command.update_goods(
        **goods_data.model_dump()
    )
    return command_result


async def delete_goods(id: UUID) -> Goods:
    goods_command = GoodsCommands()
    command_result = await goods_command.delete_goods(id=id)
    return command_result


async def list_count_group_by_name() -> List[GoodsCountByName]:
    goods_command = GoodsCommands()
    result: List[
        GoodsCountByName
    ] = await goods_command.list_count_group_by_name()
    return result


async def list_summ_group_by_name() -> List[GoodsSummByName]:
    goods_command = GoodsCommands()
    result: List[
        GoodsSummByName
    ] = await goods_command.list_summ_group_by_name()
    return result
