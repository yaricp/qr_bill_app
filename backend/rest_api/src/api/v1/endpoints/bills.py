from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from fastapi import Depends, HTTPException

from ... import app, manager
from ...config import URLPathsConfig
from ..schemas.bill import (Bill, BillCreate, BillCreateByURL, BillCreateForm,
                            BillUpdate)
from ..schemas.goods import Goods
from ..schemas.user_product import UncategorizedUserProduct
from ..services.bill import (create_bill, delete_bill, get_all_bills, get_bill,
                             get_month_summ, get_uncategorized_goods_bill,
                             get_uncategorized_product, parse_link_bill,
                             update_bill)


@app.get(URLPathsConfig.PREFIX + "/bills/", tags=["Bills"], response_model=List[Bill])
async def get_all_bills_route(
    offset: int = 0, limit: int = 0, user=Depends(manager)
) -> List[Bill]:
    """Shows list of bills"""
    bills: List[Bill] = await get_all_bills(user_id=user.id, offset=offset, limit=limit)
    return bills


@app.post(
    URLPathsConfig.PREFIX + "/bills/parse_url/", tags=["Bills"], response_model=Bill
)
async def parse_url_bill_route(item_in: BillCreateByURL, user=Depends(manager)) -> Bill:
    """Parses the URL of a bill."""
    bill = await parse_link_bill(link_image_data=item_in, user_id=user.id)
    return bill


@app.post(URLPathsConfig.PREFIX + "/bills/", tags=["Bills"], response_model=Bill)
async def create_bill_route(*, item_in: BillCreateForm, user=Depends(manager)) -> Bill:
    """Creates a bill."""
    new_bill_data = BillCreate(
        seller=item_in.seller,
        product=item_in.product,
        sum=item_in.sum,
        created=datetime.now(),
        user_id=user.id,
    )
    bill = await create_bill(new_bill_data)
    return bill


@app.get(URLPathsConfig.PREFIX + "/bills/{id}", tags=["Bills"], response_model=Bill)
async def get_bill_route(id: UUID, user=Depends(manager)) -> Bill:
    """Shows bill info."""
    bill: Bill = await get_bill(id=id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


@app.get(
    URLPathsConfig.PREFIX + "/bills/{id}/uncategorized_goods/{cat_id}",
    tags=["Bills"],
    response_model=List[Goods],
)
async def uncategorized_goods_bill_cat_route(
    id: UUID, cat_id: UUID, user=Depends(manager)
) -> List[Goods]:
    """Shows uncategorized goods for bill and category"""
    goods_list: List[Goods] = await get_uncategorized_goods_bill(
        id=id, user_id=user.id, cat_id=cat_id
    )
    return goods_list


@app.get(
    URLPathsConfig.PREFIX + "/bills/{id}/uncategorized_goods/",
    tags=["Bills"],
    response_model=List[Goods],
)
async def uncategorized_goods_bill_route(
    id: UUID, user=Depends(manager)
) -> List[Goods]:
    """Shows uncategorized goods for particular bill"""
    goods_list: List[Goods] = await get_uncategorized_goods_bill(id=id, user_id=user.id)
    return goods_list


@app.put(URLPathsConfig.PREFIX + "/bills/{id}", tags=["Bills"], response_model=Bill)
async def put_bill_route(id: UUID, item_in: BillUpdate, user=Depends(manager)) -> Bill:
    """Updates the bill"""
    item_in.user_id = user.id
    bill: Bill = await update_bill(id=id, bill_data=item_in)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


@app.delete(URLPathsConfig.PREFIX + "/bills/{id}", tags=["Bills"], response_model=Bill)
async def delete_bill_route(id: UUID, user=Depends(manager)) -> Bill:
    """Deletes the bill"""
    bill: Bill = await delete_bill(id=id, user_id=user.id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


@app.get(
    URLPathsConfig.PREFIX + "/bills/{id}/uncategorized_products/",
    tags=["Bills"],
    response_model=List[UncategorizedUserProduct],
)
@app.get(
    URLPathsConfig.PREFIX + "/bills/{id}/uncategorized_products/{cat_id}",
    tags=["Bills"],
    response_model=List[UncategorizedUserProduct],
)
async def uncategorized_products_bill_cat_route(
    id: UUID, cat_id: Optional[UUID] = None, user=Depends(manager)
) -> List[UncategorizedUserProduct]:
    """
    Shows uncategorized product for a particular bill and category.
    """
    product_list: List[UncategorizedUserProduct] = await get_uncategorized_product(
        id=id, user_id=user.id, cat_id=cat_id
    )
    return product_list


@app.get(
    URLPathsConfig.PREFIX + "/bills/month_summ/{delta_month}",
    tags=["Bills"],
    response_model=Decimal,
)
async def month_summ_bill_route(delta_month: int = 0, user=Depends(manager)) -> Decimal:
    """Shows total summ by months"""
    result: Decimal = await get_month_summ(user_id=user.id, delta_month=delta_month)
    return result
