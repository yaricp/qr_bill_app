from uuid import UUID
from datetime import datetime

from ....domain.aggregates.attraction_aggregate import (
    AttractionAggregate
)
from ....app.queries.attraction_aggregate_queries import (
    AttractionAggregatesQuery
)
from ....app.commands.attraction_aggregate_commands import (
    AttractionAggregateCommandUseCase
)

from ..schemas.statictic_row import StatisticRowCreate


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# ----Views----


async def get_attraction_aggregate(id: UUID) -> AttractionAggregate:
    attractions_query = AttractionAggregatesQuery()
    return await attractions_query.get_attraction_aggregate_by_id(
        id=id
    )


# ----Actions(Commands)


async def active_attraction_license(
    attraction_id: UUID, license_id: UUID
) -> AttractionAggregate:
    command = AttractionAggregateCommandUseCase()
    command_result = await command.active_attraction_license(
        attraction_id=attraction_id, license_id=license_id
    )
    return command_result


async def attraction_add_statistic_row(
    attraction_id: UUID, count_packages: int
) -> AttractionAggregate:
    command = AttractionAggregateCommandUseCase()
    command_result = await command.attraction_add_stat_row(
        created=datetime.now(),
        attraction_id=attraction_id,
        count_packages=count_packages
    )
    return command_result


# async def create_attraction_aggregate(
#     attraction_data: AttractionCreate
# ) -> AttractionAggregate:
#     command = AttractionAggregateCommandUseCase()
#     command_result = await command.create_attraction(
#         **attraction_data.model_dump()
#     )
#     return command_result
