from uuid import UUID
from typing import List, MutableSequence

from fastapi import APIRouter, Depends
# from loguru import logger

from ....domain.entities.attraction_entity import AttractionEntity

from ..services.attraction import (
    get_attraction, create_attraction, get_all_attractions,
    update_attraction, delete_attraction
)
from ..schemas.attraction import AttractionCreate, AttractionUpdate


router = APIRouter()


@router.post(
    "/", response_model=AttractionEntity
)
async def create_attraction_route(
    *, item_in: AttractionCreate
) -> str:
    """
    Create new attraction.
    """
    attraction = await create_attraction(
        attraction_data=item_in
    )
    return attraction


@router.get("/", response_model=List[AttractionEntity])
async def get_all_attractions_route():
    attractions: MutableSequence[
        AttractionEntity
    ] = await get_all_attractions()
    return attractions


@router.get("/{id}", response_model=AttractionEntity)
async def get_attraction_route(id: UUID):
    attraction: AttractionEntity = await get_attraction(id=id)
    return attraction


@router.put("/{id}", response_model=AttractionEntity)
async def put_attraction_route(
    id: UUID, item_in: AttractionUpdate
):
    item_in.id = id
    attraction: AttractionEntity = await update_attraction(
        attraction_data=item_in
    )
    return attraction


@router.delete("/{id}", response_model=AttractionEntity)
async def delete_attraction_route(id: UUID):
    result: AttractionEntity = await delete_attraction(
        id=id
    )
    return result
