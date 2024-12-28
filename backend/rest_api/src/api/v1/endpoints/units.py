from uuid import UUID
from typing import List, MutableSequence

from fastapi import APIRouter, Depends
# from loguru import logger


from ..services.unit import (
    get_unit, create_unit, get_all_units,
    update_unit, delete_unit
)
from ..schemas.unit import (
    Unit, UnitCreate, UnitUpdate
)


router = APIRouter()


@router.post(
    "/", response_model=Unit
)
async def create_unit_route(
    *, item_in: UnitCreate
) -> str:
    """
    Create new unit.
    """
    unit = await create_unit(
        unit_data=item_in
    )
    return unit


@router.get("/", response_model=List[Unit])
async def get_all_units_route():
    units: MutableSequence[
        Unit
    ] = await get_all_units()
    return units


@router.get("/{id}", response_model=Unit)
async def get_unit_route(id: UUID):
    unit: Unit = await get_unit(id=id)
    return unit


@router.put("/{id}", response_model=Unit)
async def put_unit_route(
    id: UUID, item_in: UnitUpdate
):
    item_in.id = id
    unit: Unit = await update_unit(
        unit_data=item_in
    )
    return unit


@router.delete("/{id}", response_model=Unit)
async def delete_unit_route(id: UUID):
    result: Unit = await delete_unit(
        id=id
    )
    return result
