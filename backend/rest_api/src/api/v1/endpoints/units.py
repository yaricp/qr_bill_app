from uuid import UUID
from typing import List

from fastapi import Depends, HTTPException

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
    """ Creates a new unit """
    return await create_unit(unit_data=item_in)


@app.get(
    URLPathsConfig.PREFIX + "/units/",
    tags=['Units'],
    response_model=List[Unit]
)
async def get_all_units_route(user=Depends(manager)) -> List[Unit]:
    """ Gets list of units """
    return await get_all_units()


@app.get(
    URLPathsConfig.PREFIX + "/units/{id}",
    tags=['Units'],
    response_model=Unit
)
async def get_unit_route(id: UUID, user=Depends(manager)) -> Unit:
    """ Gets a unit """
    unit: Unit = await get_unit(id=id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit


@app.put(
    URLPathsConfig.PREFIX + "/units/{id}",
    tags=['Units'],
    response_model=Unit
)
async def put_unit_route(
    id: UUID, item_in: UnitUpdate, user=Depends(manager)
) -> Unit:
    """ Updates a unit """
    item_in.id = id
    unit: Unit = await update_unit(unit_data=item_in)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit


@app.delete(
    URLPathsConfig.PREFIX + "/units/{id}",
    tags=['Units'],
    response_model=Unit
)
async def delete_unit_route(id: UUID, user=Depends(manager)) -> Unit:
    """ Deletes a unit """
    unit: Unit = await delete_unit(id=id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit
