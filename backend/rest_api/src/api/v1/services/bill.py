from uuid import UUID
from typing import List

from ....app.bill import BillCommands, BillQueries

from ..schemas.bill import Bill, BillUpdate, BillCreate


# -----Views-----


async def get_all_bills() -> List[Bill]:
    query: BillQueries = BillQueries()
    return await query.get_all_bills()


async def get_bill(id: UUID) -> Bill:
    query: BillQueries = BillQueries()
    return await query.get_bill(id=id)


# -------Commands-------


async def parse_link_bill(
    link: str, user_id: UUID
) -> Bill:
    bill_commands: BillCommands = BillCommands()
    return await bill_commands.parse_link_save_bill(link)


async def create_bill(bill_data: BillCreate) -> Bill:
    bill_commands: BillCommands = BillCommands()
    return await bill_commands.get_or_create(bill_data)


async def scan_qr_picture(file_path_picture: str):
    pass


async def update_bill(id: UUID, bill_data: BillUpdate) -> Bill:
    return None


async def delete_bill(id: UUID) -> Bill:
    return None
