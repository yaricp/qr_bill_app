from uuid import UUID
from typing import List

from ....app.bill import BillCommands, BillQueries

from ..schemas.bill import Bill, BillUpdate


# -----Views-----


async def get_all_bills() -> List[Bill]:
    query: BillQueries = BillQueries()
    return await query.get_all_bills()


async def get_bill(id: UUID) -> Bill:
    query: BillQueries = BillQueries()
    return await query.get_bill(id=id)


# -------Commands-------


async def parse_link_bill(link: str) -> Bill:
    bill_utils: BillCommands = BillCommands()
    return await bill_utils.parse_link_save_bill(link)


async def scan_qr_picture(file_path_picture: str):
    pass


async def update_bill(id: UUID, unit_data: BillUpdate) -> Bill:
    return None


async def delete_bill(id: UUID) -> Bill:
    return None
