from uuid import UUID
from typing import List

from ....app.unit import UnitQueries, UnitCommands

from ..schemas.unit import (
    Unit, UnitCreate, UnitUpdate
)


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# -------Views---------


async def get_all_units() -> List[Unit]:
    unit_views: UnitQueries = UnitQueries()
    return await unit_views.get_all_units()


async def get_unit(id: UUID) -> Unit:
    unit_views: UnitQueries = UnitQueries()
    return await unit_views.get_unit(id=id)


# --------Actions (commands) ---------


async def create_unit(
    unit_data: UnitCreate
) -> Unit:
    unit_command = UnitCommands()
    command_result = await unit_command.create_unit(
        **unit_data.model_dump()
    )
    return command_result


async def update_unit(
    unit_data: UnitUpdate
) -> Unit:
    unit_command = UnitCommands()
    command_result = await unit_command.update_unit(
        **unit_data.model_dump()
    )
    return command_result


async def delete_unit(id: UUID) -> Unit:
    unit_command = UnitCommands()
    command_result = await unit_command.delete_unit(id=id)
    return command_result
