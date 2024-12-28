from uuid import UUID
from typing import List

from ....app.seller import SellerQueries, SellerCommands

from ..schemas.seller import (
    Seller, SellerCreate, SellerUpdate
)


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# -----Views-----


async def get_all_sellers() -> List[Seller]:
    query: SellerQueries = SellerQueries()
    return await query.get_all_sellers()


async def get_seller(id: UUID) -> Seller:
    query: SellerQueries = SellerQueries()
    return await query.get_seller(id=id)


# ------Actons(Commands)-------


async def create_seller(
    seller_data: SellerCreate
) -> Seller:
    command = SellerCommands()
    command_result = await command.create_seller(
        **seller_data.model_dump()
    )
    return command_result


async def update_seller(
    id: UUID, seller_data: SellerUpdate
) -> Seller:

    command = SellerCommands()
    command_result = await command.update_seller(
        **seller_data.model_dump()
    )
    return command_result


async def delete_seller(id: UUID) -> Seller:
    command = SellerCommands()
    command_result = await command.delete_seller(id=id)
    return command_result
