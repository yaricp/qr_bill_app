from uuid import UUID
from typing import List, MutableSequence

from fastapi import APIRouter, Depends
# from loguru import logger


from ..services.purchase import (
    get_purchase, create_purchase, get_all_purchases,
    update_purchase, delete_purchase
)
from ..schemas.purchase import (
    Purchase, PurchaseCreate, PurchaseUpdate
)


router = APIRouter()


@router.post(
    "/", response_model=Purchase
)
async def create_purchase_route(
    *, item_in: PurchaseCreate
) -> str:
    """
    Create new purchase.
    """
    purchase = await create_purchase(
        purchase_data=item_in
    )
    return purchase


@router.get("/", response_model=List[Purchase])
async def get_all_purchases_route():
    purchases: MutableSequence[
        Purchase
    ] = await get_all_purchases()
    return purchases


@router.get("/{id}", response_model=Purchase)
async def get_purchase_route(id: UUID):
    purchase: Purchase = await get_purchase(id=id)
    return purchase


@router.put("/{id}", response_model=Purchase)
async def put_purchase_route(
    id: UUID, item_in: PurchaseUpdate
):
    item_in.id = id
    purchase: Purchase = await update_purchase(
        purchase_data=item_in
    )
    return purchase


@router.delete("/{id}", response_model=Purchase)
async def delete_purchase_route(id: UUID):
    result: Purchase = await delete_purchase(
        id=id
    )
    return result
