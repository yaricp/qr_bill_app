from uuid import UUID
from typing import List, MutableSequence
from loguru import logger

from fastapi import Depends

from ... import app, manager
from ...config import URLPathsConfig
from ..services.seller import (
    get_seller, create_seller,
    update_seller, delete_seller, get_all_sellers,
    list_summ_bills_group_by_name_seller,
    list_count_bills_group_by_name_seller,
    list_count_goods_group_by_name_seller
)
from ..schemas.seller import (
    Seller, SellerCreate, SellerUpdate,
    CountBillsByNameSeller, CountGoodsByNameSeller,
    SummBillsByNameSeller
)


@app.post(
    URLPathsConfig.PREFIX + "/sellers/",
    tags=['Sellers'],
    response_model=Seller
)
async def create_seller_route(
    item_in: SellerCreate, user=Depends(manager)
) -> Seller:
    """
    Create new seller.
    """
    seller = await create_seller(item_in)
    return seller


@app.get(
    URLPathsConfig.PREFIX + "/sellers/",
    tags=['Sellers'],
    response_model=List[Seller]
)
async def get_all_sellers_route(user=Depends(manager)):
    sellers: MutableSequence[Seller] = await get_all_sellers()
    return sellers


@app.get(
    URLPathsConfig.PREFIX + "/sellers/{id}",
    tags=['Sellers'],
    response_model=Seller
)
async def get_seller_route(id: UUID, user=Depends(manager)):
    seller: Seller = await get_seller(id=id)
    return seller


@app.put(
    URLPathsConfig.PREFIX + "/sellers/{id}",
    tags=['Sellers'],
    response_model=Seller
)
async def update_seller_route(
    id: UUID, item_in: SellerUpdate, user=Depends(manager)
):
    seller: Seller = await update_seller(
        id=id, seller_data=item_in
    )
    return seller


@app.delete(
    URLPathsConfig.PREFIX + "/sellers/{id}",
    tags=['Sellers'],
    response_model=Seller
)
async def delete_seller_route(id: UUID, user=Depends(manager)):
    seller: Seller = await delete_seller(id=id)
    return seller


@app.get(
    URLPathsConfig.PREFIX + "/sellers/count_bills_by_name/",
    tags=['Sellers'],
    response_model=List[CountBillsByNameSeller]
)
async def count_bills_by_name_seller_route(
    first_of: int = 0, user=Depends(manager)
) -> List[CountBillsByNameSeller]:
    logger.info(f"first_of: {first_of}")
    result: List[
        CountBillsByNameSeller
    ] = await list_count_bills_group_by_name_seller(
        first_of=first_of, user_id=user.id
    )
    return result


@app.get(
    URLPathsConfig.PREFIX + "/sellers/summ_bills_by_name/",
    tags=['Sellers'],
    response_model=List[SummBillsByNameSeller]
)
async def summ_bills_by_name_seller_route(
    first_of: int = 0, user=Depends(manager)
) -> List[SummBillsByNameSeller]:
    result: List[
        SummBillsByNameSeller
    ] = await list_summ_bills_group_by_name_seller(
        first_of=first_of, user_id=user.id
    )
    return result


@app.get(
    URLPathsConfig.PREFIX + "/sellers/count_goods_by_name/",
    tags=['Sellers'],
    response_model=List[CountGoodsByNameSeller]
)
async def count_goods_order_by_seller_route(
    first_of: int = 0, user=Depends(manager)
) -> List[CountGoodsByNameSeller]:
    result: List[
        CountGoodsByNameSeller
    ] = await list_count_goods_group_by_name_seller(
        first_of=first_of, user_id=user.id
    )
    return result
