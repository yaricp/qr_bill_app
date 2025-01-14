from uuid import UUID
from typing import List, MutableSequence

from fastapi import Depends

from ... import app, manager
from ...config import URLPathsConfig
from ..services.unit import (
    get_unit, create_unit, get_all_units,
    update_unit, delete_unit
)
from ..schemas.unit import (
    Unit, UnitCreate, UnitUpdate
)


@app.post(
    URLPathsConfig.PREFIX + "/units/",
    tags=['Units'],
    response_model=Unit
)
async def create_unit_route(
    item_in: UnitCreate, user=Depends(manager)
) -> str:
    """
    Create new unit.
    """
    unit = await create_unit(unit_data=item_in)
    return unit


@app.get(
    URLPathsConfig.PREFIX + "/units/",
    tags=['Units'],
    response_model=List[Unit]
)
async def get_all_units_route(user=Depends(manager)):
    units: List[Unit] = await get_all_units()
    return units


@app.get(
    URLPathsConfig.PREFIX + "/units/{id}",
    tags=['Units'],
    response_model=Unit
)
async def get_unit_route(id: UUID, user=Depends(manager)):
    unit: Unit = await get_unit(id=id)
    return unit


@app.put(
    URLPathsConfig.PREFIX + "/units/{id}",
    tags=['Units'],
    response_model=Unit
)
async def put_unit_route(
    id: UUID, item_in: UnitUpdate, user=Depends(manager)
):
    item_in.id = id
    unit: Unit = await update_unit(unit_data=item_in)
    return unit


@app.delete(
    URLPathsConfig.PREFIX + "/units/{id}",
    tags=['Units'],
    response_model=Unit
)
async def delete_unit_route(id: UUID, user=Depends(manager)):
    result: Unit = await delete_unit(id=id)
    return result
