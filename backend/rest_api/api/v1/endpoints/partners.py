from uuid import UUID
from typing import List, MutableSequence

from fastapi import APIRouter
# from loguru import logger

from ....domain.entities.partner_entity import PartnerEntity

from ..services.partner import (
    get_partner, create_partner, get_all_partners, update_partner,
    delete_partner
)
from ..schemas.partner import PartnerCreate, PartnerUpdate


router = APIRouter()


@router.post("/", response_model=PartnerEntity)
async def create_partner_route(*, item_in: PartnerCreate) -> PartnerEntity:
    """
    Create new partner.
    """
    partner = await create_partner(partner_data=item_in)
    return partner


@router.get("/", response_model=List[PartnerEntity])
async def get_all_partners_route():
    partners: MutableSequence[PartnerEntity] = await get_all_partners()
    return partners


@router.get("/{id}", response_model=PartnerEntity)
async def get_partner_route(id: UUID):
    partner: PartnerEntity = await get_partner(id=id)
    return partner


@router.put("/{id}", response_model=PartnerEntity)
async def update_partner_route(
    id: UUID, item_in: PartnerUpdate
):
    partner: PartnerEntity = await update_partner(
        partner_data=item_in
    )
    return partner


@router.delete("/{id}", response_model=PartnerEntity)
async def delete_partner_route(id: UUID):
    partner: PartnerEntity = await delete_partner(
        id=id
    )
    return partner
