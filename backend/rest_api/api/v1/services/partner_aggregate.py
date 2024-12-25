from uuid import UUID
from datetime import datetime

from ....domain.aggregates.partner_aggregate import (
    PartnerAggregate
)
from ....app.queries.partner_aggregate_queries import (
    PartnerAggregatesQuery
)
from ....app.commands.partner_aggregate_commands import (
    PartnerAggregateCommandUseCase
)

from ..schemas.partner_aggregate import PartnerAggregateCreate


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# ----Views----


async def get_partner_aggregate(id: UUID) -> PartnerAggregate:
    partners_query = PartnerAggregatesQuery()
    return await partners_query.get_partner_aggregate_by_id(
        id=id
    )


# ----Actions(Commands)


async def create_partner_aggregate(
    new_partner_aggregate: PartnerAggregateCreate
) -> PartnerAggregate:
    command = PartnerAggregateCommandUseCase()
    command_result = await command.create_partner_aggregate(
        **new_partner_aggregate.model_dump()
    )
    return command_result
