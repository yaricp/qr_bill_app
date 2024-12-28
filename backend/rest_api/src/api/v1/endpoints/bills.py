from uuid import UUID
from typing import List, MutableSequence

from fastapi import APIRouter, Depends

from ..services.bill import (
    parse_link_bill, scan_qr_picture
)
from ..schemas.bill import Bill, BillCreateByURL


router = APIRouter()


@router.post(
    "/", response_model=Bill
)
async def parse_url_bill_route(
    *, item_in: BillCreateByURL
) -> Bill:
    """
    Parse url link of bill.
    """
    bill = await parse_link_bill(link=item_in.link)
    return bill
