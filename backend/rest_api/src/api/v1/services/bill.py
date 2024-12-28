# from uuid import UUID
from typing import List

from ....app.bill import BillCommands

from ..schemas.bill import Bill


async def parse_link_bill(link: str) -> List[Bill]:
    bill_utils: BillCommands = BillCommands()
    return await bill_utils.parse_link_save_bill(link)


async def scan_qr_picture(file_path_picture: str):
    pass
