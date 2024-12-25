from uuid import UUID
from typing import List

from ....app.purchase import PurchaseQueries, PurchaseCommands

from ..schemas.purchase import (
    Purchase, PurchaseCreate, PurchaseUpdate
)


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# -------Views---------


async def get_all_purchases() -> List[Purchase]:
    purchases_views: PurchaseQueries = PurchaseQueries()
    return await purchases_views.get_all_purchases()


async def get_purchase(id: UUID) -> Purchase:
    purchases_views: PurchaseQueries = PurchaseQueries()
    return await purchases_views.get_purchase(purchase_id=id)


# --------Actions (commands) ---------


async def create_purchase(
    purchase_data: PurchaseCreate
) -> Purchase:
    purchase_command = PurchaseCommands()
    command_result = await purchase_command.create_purchase(
        **purchase_data.model_dump()
    )
    return command_result


async def update_purchase(
    purchase_data: PurchaseUpdate
) -> Purchase:
    purchase_command = PurchaseCommands()
    command_result = await purchase_command.update_purchase(
        **purchase_data.model_dump()
    )
    return command_result


async def delete_purchase(id: UUID) -> Purchase:
    purchase_command = PurchaseCommands()
    command_result = await purchase_command.delete_purchase(id=id)
    return command_result
