from uuid import UUID
from typing import List, MutableSequence

from fastapi import Depends
# APIRouter,

from ... import app, manager
from ..services.bill import (
    get_bill, get_all_bills, parse_link_bill,
    update_bill, delete_bill, scan_qr_picture, create_bill
)
from ..schemas.bill import (
    Bill, BillCreateByURL, BillUpdate, BillCreate
)
from ...config import URLPathsConfig


@app.get(
    URLPathsConfig.PREFIX + "/bills", tags=['Bills'], response_model=List[Bill]
)
async def get_all_bills_route(user=Depends(manager)) -> List[Bill]:
    bills: List[Bill] = await get_all_bills()
    return bills


@app.post(
    URLPathsConfig.PREFIX + "/bills/parse_url", tags=['Bills'], response_model=Bill
)
async def parse_url_bill_route(
    item_in: BillCreateByURL, user=Depends(manager)
) -> Bill:
    """
    Parse url link of bill.
    """
    bill = await parse_link_bill(
        link=item_in.link, user_id=user.id
    )
    return bill


@app.post(
    URLPathsConfig.PREFIX + "/bills", tags=['Bills'], response_model=Bill
)
async def create_bill_route(
    *, item_in: BillCreate, user=Depends(manager)
) -> Bill:
    """
    Create bill.
    """
    bill = await create_bill(item_in)
    return bill


@app.get(
    URLPathsConfig.PREFIX + "/bills/{id}", tags=['Bills'], response_model=Bill
)
async def get_bill_route(id: UUID, user=Depends(manager)) -> Bill:
    bill: Bill = await get_bill(id=id)
    return bill


@app.put(
    URLPathsConfig.PREFIX + "/bills/{id}", tags=['Bills'], response_model=Bill
)
async def put_bill_route(
    id: UUID, item_in: BillUpdate, user=Depends(manager)
) -> Bill:
    bill: Bill = await update_bill(
        id=id, unit_data=item_in
    )
    return bill


@app.delete(
    URLPathsConfig.PREFIX + "/bills/{id}", tags=['Bills'], response_model=Bill
)
async def delete_bill_route(id: UUID, user=Depends(manager)) -> Bill:
    bill: Bill = await delete_bill(id=id)
    return bill
