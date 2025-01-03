from uuid import UUID
from typing import List, MutableSequence

from fastapi import Depends

from ... import app, manager
from ...config import URLPathsConfig
from ..services.seller import (
    get_seller, create_seller, get_all_sellers,
    update_seller, delete_seller, order_by_count_goods
)
from ..schemas.seller import (
    Seller, SellerCreate, SellerUpdate, SellerByCountGoods
)


@app.post(
    URLPathsConfig.PREFIX + "/sellers",
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
    URLPathsConfig.PREFIX + "/sellers",
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
    URLPathsConfig.PREFIX + "/sellers/order_by_count_goods/",
    tags=['Sellers'],
    response_model=List[SellerByCountGoods]
)
async def order_by_count_goods_route(user=Depends(manager)) -> List[SellerByCountGoods]:
    result: List[SellerByCountGoods] = await order_by_count_goods()
    return result
