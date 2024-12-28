from uuid import UUID
from typing import List, MutableSequence

from fastapi import APIRouter

from ..services.seller import (
    get_seller, create_seller, get_all_sellers,
    update_seller, delete_seller
)
from ..schemas.seller import (
    Seller, SellerCreate, SellerUpdate
)


router = APIRouter()


@router.post("/", response_model=Seller)
async def create_seller_route(
    *, item_in: SellerCreate
) -> str:
    """
    Create new seller.
    """
    seller = await create_seller(item_in)
    return seller


@router.get("/", response_model=List[Seller])
async def get_all_sellers_route():
    sellers: MutableSequence[Seller] = await get_all_sellers()
    return sellers


@router.get("/{id}", response_model=Seller)
async def get_seller_route(id: UUID):
    seller: Seller = await get_seller(id=id)
    return seller


@router.put("/{id}", response_model=Seller)
async def update_seller_route(
    id: UUID, item_in: SellerUpdate
):
    seller: Seller = await update_seller(
        id=id, seller_data=item_in
    )
    return seller


@router.delete("/{id}", response_model=Seller)
async def delete_seller_route(id: UUID):
    seller: Seller = await delete_seller(id=id)
    return seller
