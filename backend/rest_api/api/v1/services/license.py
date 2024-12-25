from uuid import UUID
from typing import List

from ....domain.entities.license_entity import (
    LicenseEntity
)
from ....app.queries.license_queries import LicensesQuery
from ....app.commands.license_commands import LicenseCommandUseCase

from ..schemas.license import LicenseCreate, LicenseUpdate


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# -----Views-----


async def get_all_licenses() -> List[LicenseEntity]:
    query: LicensesQuery = LicensesQuery()
    return await query.get_all_licenses()


async def get_license(id: UUID) -> LicenseEntity:
    query: LicensesQuery = LicensesQuery()
    return await query.get_license(id=id)


# ------Actons(Commands)-------


async def create_license(
    license_data: LicenseCreate
) -> LicenseEntity:
    command = LicenseCommandUseCase()
    command_result = await command.create_license(
        **license_data.model_dump()
    )
    return command_result


async def update_license(
    id: UUID, license_data: LicenseUpdate
) -> LicenseEntity:

    command = LicenseCommandUseCase()
    command_result = await command.update_license(
        **license_data.model_dump()
    )
    return command_result


async def delete_license(id: UUID) -> LicenseEntity:
    command = LicenseCommandUseCase()
    command_result = await command.delete_license(id=id)
    return command_result
