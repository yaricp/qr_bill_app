from uuid import UUID
from typing import List

from fastapi import Depends, HTTPException

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
    tags=["Sellers"],
    response_model=Seller
)
async def create_seller_route(
    item_in: SellerCreate, user=Depends(manager)
) -> Seller:
    """ Create new seller """
    return await create_seller(item_in)


@app.get(
    URLPathsConfig.PREFIX + "/sellers/",
    tags=["Sellers"],
    response_model=List[Seller]
)
async def get_all_sellers_route(
    offset: int = 0, limit: int = 0, user=Depends(manager)
) -> List[Seller]:
    """ Gets list of sellers """
    return await get_all_sellers(
        user_id=user.id, offset=offset, limit=limit
    )


@app.get(
    URLPathsConfig.PREFIX + "/sellers/{id}",
    tags=["Sellers"],
    response_model=Seller
)
async def get_seller_route(id: UUID, user=Depends(manager)):
    """ Gets seller info """
    seller: Seller = await get_seller(id=id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller


@app.put(
    URLPathsConfig.PREFIX + "/sellers/{id}",
    tags=["Sellers"],
    response_model=Seller
)
async def update_seller_route(
    id: UUID, item_in: SellerUpdate, user=Depends(manager)
):
    """ Updates seller info """
    seller: Seller = await update_seller(
        id=id, seller_data=item_in
    )
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller


@app.delete(
    URLPathsConfig.PREFIX + "/sellers/{id}",
    tags=["Sellers"],
    response_model=Seller
)
async def delete_seller_route(id: UUID, user=Depends(manager)):
    """ Deletes seller """
    seller: Seller = await delete_seller(id=id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller


@app.get(
    URLPathsConfig.PREFIX + "/sellers/count_bills_by_name/",
    tags=["Sellers"],
    response_model=List[CountBillsByNameSeller]
)
async def count_bills_by_name_seller_route(
    first_of: int = 0, user=Depends(manager)
) -> List[CountBillsByNameSeller]:
    """ Gets list of bills grouped by name seller """
    return await list_count_bills_group_by_name_seller(
        first_of=first_of, user_id=user.id
    )


@app.get(
    URLPathsConfig.PREFIX + "/sellers/summ_bills_by_name/",
    tags=["Sellers"],
    response_model=List[SummBillsByNameSeller]
)
async def summ_bills_by_name_seller_route(
    first_of: int = 0, user=Depends(manager)
) -> List[SummBillsByNameSeller]:
    """ Gets a list of bill amounts grouped by seller name """
    return await list_summ_bills_group_by_name_seller(
        first_of=first_of, user_id=user.id
    )


@app.get(
    URLPathsConfig.PREFIX + "/sellers/count_goods_by_name/",
    tags=["Sellers"],
    response_model=List[CountGoodsByNameSeller]
)
async def count_goods_order_by_seller_route(
    first_of: int = 0, user=Depends(manager)
) -> List[CountGoodsByNameSeller]:
    """ Gets a list of goods quantities, grouped by seller name """
    return await list_count_goods_group_by_name_seller(
        first_of=first_of, user_id=user.id
    )
