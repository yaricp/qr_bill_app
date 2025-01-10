from uuid import UUID
from typing import List

from ....app.bill import BillCommands, BillQueries

from ..schemas.bill import Bill, BillUpdate, BillCreate
from ..schemas.goods import Goods


# -----Views-----


async def get_all_bills(user_id: UUID) -> List[Bill]:
    query: BillQueries = BillQueries()
    return await query.get_all_bills(user_id=user_id)


async def get_bill(id: UUID) -> Bill:
    query: BillQueries = BillQueries()
    return await query.get_bill(id=id)


async def get_uncategorized_goods_bill(
    id: UUID, user_id: UUID, cat_id: UUID | None = None
) -> List[Goods]:
    query: BillQueries = BillQueries()
    return await query.get_uncategorized_goods(
        bill_id=id, user_id=user_id, cat_id=cat_id
    )

# -------Commands-------


async def parse_link_bill(
    link: str, user_id: UUID
) -> Bill:
    bill_commands: BillCommands = BillCommands()
    return await bill_commands.parse_link_save_bill(
        income_link=link, user_id=user_id
    )


async def create_bill(
    bill_data: BillCreate
) -> Bill:
    bill_commands: BillCommands = BillCommands()
    return await bill_commands.get_or_create(
        incoming_item=bill_data
    )


async def scan_qr_picture(file_path_picture: str):
    pass


async def update_bill(
    id: UUID, bill_data: BillUpdate
) -> Bill:
    return None


async def delete_bill(id: UUID, user_id: UUID) -> Bill:
    return None
