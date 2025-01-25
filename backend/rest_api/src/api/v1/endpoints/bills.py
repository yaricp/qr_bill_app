from uuid import UUID
from typing import List, Optional

from fastapi import Depends

from ... import app, manager
from ...config import URLPathsConfig
from ..services.bill import (
    get_bill, get_all_bills, parse_link_bill,
    update_bill, delete_bill, scan_qr_picture,
    create_bill, get_uncategorized_goods_bill,
    get_uncategorized_product
)
from ..schemas.bill import (
    Bill, BillCreateByURL, BillUpdate, BillCreate
)
from ..schemas.goods import Goods
from ..schemas.user_product import UncategorizedUserProduct


@app.get(
    URLPathsConfig.PREFIX + "/bills/",
    tags=['Bills'], response_model=List[Bill]
)
async def get_all_bills_route(user=Depends(manager)) -> List[Bill]:
    bills: List[Bill] = await get_all_bills(user_id=user.id)
    return bills


@app.post(
    URLPathsConfig.PREFIX + "/bills/parse_url/",
    tags=['Bills'], response_model=Bill
)
async def parse_url_bill_route(
    item_in: BillCreateByURL, user=Depends(manager)
) -> Bill:
    """
    Parse url link of bill.
    """
    bill = await parse_link_bill(
        link_image_data=item_in, user_id=user.id
    )
    return bill


@app.post(
    URLPathsConfig.PREFIX + "/bills/",
    tags=['Bills'], response_model=Bill
)
async def create_bill_route(
    *, item_in: BillCreate, user=Depends(manager)
) -> Bill:
    """
    Create bill.
    """
    item_in.user_id = user.id
    bill = await create_bill(item_in)
    return bill


@app.get(
    URLPathsConfig.PREFIX + "/bills/{id}",
    tags=['Bills'], response_model=Bill
)
async def get_bill_route(id: UUID, user=Depends(manager)) -> Bill:
    bill: Bill = await get_bill(id=id)
    return bill


@app.get(
    URLPathsConfig.PREFIX + "/bills/{id}/uncategorized_goods/{cat_id}",
    tags=['Bills'],
    response_model=List[Goods]
)
async def uncategorized_goods_bill_cat_route(
    id: UUID, cat_id: UUID, user=Depends(manager)
) -> List[Goods]:
    goods_list: List[Goods] = await get_uncategorized_goods_bill(
        id=id, user_id=user.id, cat_id=cat_id
    )
    return goods_list


@app.get(
    URLPathsConfig.PREFIX + "/bills/{id}/uncategorized_goods/",
    tags=['Bills'],
    response_model=List[Goods]
)
async def uncategorized_goods_bill_route(
    id: UUID, user=Depends(manager)
) -> List[Goods]:
    goods_list: List[Goods] = await get_uncategorized_goods_bill(
        id=id, user_id=user.id
    )
    return goods_list


@app.put(
    URLPathsConfig.PREFIX + "/bills/{id}",
    tags=['Bills'], response_model=Bill
)
async def put_bill_route(
    id: UUID, item_in: BillUpdate, user=Depends(manager)
) -> Bill:
    item_in.user_id = user.id
    bill: Bill = await update_bill(
        id=id, bill_data=item_in
    )
    return bill


@app.delete(
    URLPathsConfig.PREFIX + "/bills/{id}",
    tags=['Bills'], response_model=Bill
)
async def delete_bill_route(id: UUID, user=Depends(manager)) -> Bill:
    bill: Bill = await delete_bill(id=id, user_id=user.id)
    return bill


@app.get(
    URLPathsConfig.PREFIX + "/bills/{id}/uncategorized_products/",
    tags=['Bills'],
    response_model=List[UncategorizedUserProduct]
)
@app.get(
    URLPathsConfig.PREFIX + "/bills/{id}/uncategorized_products/{cat_id}",
    tags=['Bills'],
    response_model=List[UncategorizedUserProduct]
)
async def uncategorized_products_bill_cat_route(
    id: UUID,
    cat_id: Optional[UUID] = None,
    user=Depends(manager)
) -> List[UncategorizedUserProduct]:
    product_list: List[UncategorizedUserProduct] = await get_uncategorized_product(
        id=id, user_id=user.id, cat_id=cat_id
    )
    return product_list
