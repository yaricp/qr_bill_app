from uuid import UUID
from decimal import Decimal
from typing import List

from ....app.bill import BillCommands, BillQueries

from ..schemas.bill import (
    Bill, BillUpdate, BillCreate, BillCreateByURL
)
from ..schemas.goods import Goods
from ..schemas.user_product import UncategorizedUserProduct


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


async def get_uncategorized_product(
     id: UUID, user_id: UUID, cat_id: UUID | None = None
) -> List[UncategorizedUserProduct]:
    query: BillQueries = BillQueries()
    return await query.get_uncategorized_product(
        bill_id=id, user_id=user_id, cat_id=cat_id
    )


async def get_month_summ(
    user_id: UUID, delta_month: int
) -> Decimal:
    query: BillQueries = BillQueries()
    return await query.get_month_summ(
        user_id=user_id, delta_month=delta_month
    )


# -------Commands-------


async def parse_link_bill(
    link_image_data: BillCreateByURL, user_id: UUID
) -> Bill:
    bill_commands: BillCommands = BillCommands()
    return await bill_commands.parse_link_save_bill(
        income_link=link_image_data, user_id=user_id
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
