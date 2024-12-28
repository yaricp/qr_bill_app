from uuid import UUID
from typing import List, MutableSequence

from fastapi import APIRouter, Depends

from ..services.bill import (
    get_bill, get_all_bills, parse_link_bill,
    update_bill, delete_bill, scan_qr_picture
)
from ..schemas.bill import (
    Bill, BillCreateByURL, BillUpdate
)


router = APIRouter()


@router.post(
    "/parse_url", response_model=Bill
)
async def parse_url_bill_route(
    *, item_in: BillCreateByURL
) -> Bill:
    """
    Parse url link of bill.
    """
    bill = await parse_link_bill(link=item_in.link)
    return bill


@router.get("/", response_model=List[Bill])
async def get_all_bills_route() -> List[Bill]:
    bills: List[Bill] = await get_all_bills()
    return bills


@router.get("/{id}", response_model=Bill)
async def get_bill_route(id: UUID) -> Bill:
    bill: Bill = await get_bill(id=id)
    return bill


@router.put("/{id}", response_model=Bill)
async def put_bill_route(id: UUID, item_in: BillUpdate) -> Bill:
    bill: Bill = await update_bill(
        id=id, unit_data=item_in
    )
    return bill


@router.delete("/{id}", response_model=Bill)
async def delete_bill_route(id: UUID) -> Bill:
    bill: Bill = await delete_bill(id=id)
    return bill
