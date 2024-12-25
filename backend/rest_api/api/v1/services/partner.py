from uuid import UUID
from typing import List

from ....domain.entities.partner_entity import (
    PartnerEntity
)
from ....app.queries.partner_queries import PartnersQuery
from ....app.commands.partner_commands import PartnerCommandUseCase

from ..schemas.partner import PartnerCreate, PartnerUpdate


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# -------Views---------


async def get_all_partners() -> List[PartnerEntity]:
    partners_views: PartnersQuery = PartnersQuery()
    return await partners_views.get_all_partners()


async def get_partner(id: UUID) -> PartnerEntity:
    partners_views: PartnersQuery = PartnersQuery()
    return await partners_views.get_partner(partner_id=id)


# --------Actions (commands) ---------


async def create_partner(
    partner_data: PartnerCreate
) -> PartnerEntity:
    partner_command = PartnerCommandUseCase()
    command_result = await partner_command.create_partner(
        **partner_data.model_dump()
    )
    return command_result


async def update_partner(
    partner_data: PartnerUpdate
) -> PartnerEntity:
    partner_command = PartnerCommandUseCase()
    command_result = await partner_command.update_partner(
        **partner_data.model_dump()
    )
    return command_result


async def delete_partner(id: UUID) -> PartnerEntity:
    partner_command = PartnerCommandUseCase()
    command_result = await partner_command.delete_partner(id=id)
    return command_result
