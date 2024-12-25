from uuid import UUID
from typing import List

from ....domain.entities.attraction_entity import (
    AttractionEntity
)
from ....domain.aggregates.attraction_aggregate import (
    AttractionAggregate
)
from ....app.queries.attraction_queries import AttractionsQuery

from ....app.commands.attraction_commands import AttractionCommandUseCase

from ..schemas.attraction import (
    AttractionCreate, AttractionUpdate
)


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# ----Views----


async def get_all_attractions() -> List[AttractionEntity]:
    attractions_views: AttractionsQuery = AttractionsQuery()
    return await attractions_views.get_all_attractions()


async def get_attraction(id: UUID) -> AttractionAggregate:
    attractions_query: AttractionsQuery = AttractionsQuery()
    return await attractions_query.get_attraction(attraction_id=id)


# -----Actions-----


async def create_attraction(
    attraction_data: AttractionCreate
) -> AttractionEntity:
    attraction_command = AttractionCommandUseCase()
    command_result = await attraction_command.create_attraction(
        **attraction_data.model_dump()
    )
    return command_result


async def update_attraction(
    attraction_data: AttractionUpdate
) -> AttractionEntity:
    attraction_command = AttractionCommandUseCase()
    command_result = await attraction_command.update_attraction(
        **attraction_data.model_dump()
    )
    return command_result


async def delete_attraction(
    id: UUID
) -> AttractionEntity:
    attraction_command = AttractionCommandUseCase()
    command_result = await attraction_command.delete_attraction(id=id)
    return command_result
