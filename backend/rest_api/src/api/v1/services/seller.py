from uuid import UUID
from typing import List

from ....app.seller import SellerQueries, SellerCommands

from ..schemas.seller import (
    Seller, SellerCreate, SellerUpdate, SellerByCountGoods,
    SellerCountByName, SellerSummByName
)


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# -----Views-----


async def get_all_sellers() -> List[Seller]:
    queries: SellerQueries = SellerQueries()
    return await queries.get_all_sellers()


async def get_seller(id: UUID) -> Seller:
    queries: SellerQueries = SellerQueries()
    return await queries.get_seller(id=id)


async def order_by_count_goods(
    first_of: int, user_id: UUID
) -> List[SellerByCountGoods]:
    queries: SellerQueries = SellerQueries()
    return await queries.get_sellers_order_by_count_goods(
        first_of=first_of, user_id=user_id
    )


async def list_count_group_by_name(
    first_of: int, user_id: UUID
) -> List[SellerCountByName]:
    queries: SellerQueries = SellerQueries()
    result: List[
        SellerCountByName
    ] = await queries.get_sellers_order_by_count_bills(
        first_of=first_of, user_id=user_id
    )
    return result


async def list_summ_group_by_name(
    first_of: int, user_id: UUID
) -> List[SellerSummByName]:
    queries: SellerQueries = SellerQueries()
    result: List[
        SellerSummByName
    ] = await queries.get_sellers_order_by_summ_bills(
        first_of=first_of, user_id=user_id
    )
    return result


# ------Actons(Commands)-------


async def create_seller(
    seller_data: SellerCreate
) -> Seller:
    command = SellerCommands()
    command_result = await command.create_seller(seller_data)
    return command_result


async def update_seller(
    id: UUID, seller_data: SellerUpdate
) -> Seller:

    command = SellerCommands()
    command_result = await command.update_seller(
        seller_data
    )
    return command_result


async def delete_seller(id: UUID) -> Seller:
    command = SellerCommands()
    command_result = await command.delete_seller(id=id)
    return command_result
