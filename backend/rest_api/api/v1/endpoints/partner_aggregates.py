from uuid import UUID
# from typing import List, MutableSequence

from fastapi import APIRouter

from ....domain.aggregates.partner_aggregate import (
    PartnerAggregate
)

from ..services.partner_aggregate import (
    get_partner_aggregate, create_partner_aggregate
)
from ..schemas.partner_aggregate import PartnerAggregateCreate

router = APIRouter()


@router.get(
    path="/{id}",
    name="Get Partner Aggregate",
    response_model=PartnerAggregate
)
async def get_partner_aggregate_route(
    id: UUID
) -> PartnerAggregate:
    partner_aggregate: PartnerAggregate = await get_partner_aggregate(
        id=id
    )
    return partner_aggregate


@router.post(
    path="/",
    name="Create a new Partner Aggregate",
    response_model=PartnerAggregate
)
async def statictic_row_add_route(
    new_partner_aggregate: PartnerAggregateCreate
) -> PartnerAggregate:
    partner_aggregate = await create_partner_aggregate(
        new_partner_aggregate=new_partner_aggregate
    )
    return partner_aggregate
