from uuid import UUID
from typing import List

from ....app.seller import SellerQueries, SellerCommands

from ..schemas.seller import (
    Seller, SellerCreate, SellerUpdate,
    CountGoodsByNameSeller, CountBillsByNameSeller,
    SummBillsByNameSeller
)


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# -----Views-----


async def get_all_sellers(
    user_id: UUID, offset: int = 0, limit: int = 0
) -> List[Seller]:
    queries: SellerQueries = SellerQueries()
    return await queries.get_all_sellers(
        user_id=user_id, offset=offset, limit=limit
    )


async def get_seller(id: UUID) -> Seller:
    queries: SellerQueries = SellerQueries()
    return await queries.get_seller(id=id)


async def list_count_goods_group_by_name_seller(
    first_of: int, user_id: UUID
) -> List[CountGoodsByNameSeller]:
    queries: SellerQueries = SellerQueries()
    result: List[
        CountGoodsByNameSeller
    ] = await queries.get_sellers_order_by_count_goods(
        first_of=first_of, user_id=user_id
    )
    return result


async def list_count_bills_group_by_name_seller(
    first_of: int, user_id: UUID
) -> List[CountBillsByNameSeller]:
    queries: SellerQueries = SellerQueries()
    result: List[
        CountBillsByNameSeller
    ] = await queries.get_sellers_order_by_count_bills(
        first_of=first_of, user_id=user_id
    )
    return result


async def list_summ_bills_group_by_name_seller(
    first_of: int, user_id: UUID
) -> List[SummBillsByNameSeller]:
    queries: SellerQueries = SellerQueries()
    result: List[
        SummBillsByNameSeller
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
