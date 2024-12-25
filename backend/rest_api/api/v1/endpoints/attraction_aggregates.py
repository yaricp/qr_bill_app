from uuid import UUID
# from typing import List, MutableSequence

from fastapi import APIRouter

from ....domain.aggregates.attraction_aggregate import (
    AttractionAggregate
)

from ..services.attraction_aggregate import (
    get_attraction_aggregate, active_attraction_license,
    attraction_add_statistic_row
)
# from ..schemas.attraction import AttractionCreate, AttractionUpdate
from ..schemas.statictic_row import StatisticRowCreate

router = APIRouter()


# @router.post(
#     "/", response_model=AttractionAggregate
# )
# async def create_attraction_aggregate_route(
#     *, item_in: AttractionCreate
# ) -> str:
#     """
#     Create new attraction aggregates.
#     """
#     attraction = await create_attraction(item_in)
#     return attraction


@router.get(
    path="/{id}",
    name="Get Aggregate",
    response_model=AttractionAggregate
)
async def get_attraction_aggregate_route(
    id: UUID
) -> AttractionAggregate:
    attraction_aggregate: AttractionAggregate = await get_attraction_aggregate(
        id=id
    )
    return attraction_aggregate


@router.put(
    path="/{id}/active_license/{license_id}",
    name="Activate License",
    response_model=AttractionAggregate
)
async def activate_license_route(
    id: UUID, license_id: UUID
) -> AttractionAggregate:
    attraction_aggregate = await active_attraction_license(
        license_id=license_id,
        attraction_id=id
    )
    return attraction_aggregate


@router.post(
    path="/{id}/statistic_row_add",
    name="Add Statistic Row",
    response_model=AttractionAggregate
)
async def statictic_row_add_route(
    id: UUID, count_packages: int
) -> AttractionAggregate:
    attraction_aggregate = await attraction_add_statistic_row(
        attraction_id=id,
        count_packages=count_packages
    )
    return attraction_aggregate
