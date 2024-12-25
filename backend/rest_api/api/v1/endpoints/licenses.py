from uuid import UUID
from typing import List, MutableSequence

from fastapi import APIRouter

from ....domain.entities.license_entity import LicenseEntity

from ..services.license import (
    get_license, create_license, get_all_licenses,
    update_license, delete_license
)
from ..schemas.license import (
    LicenseCreate, LicenseUpdate
)


router = APIRouter()


@router.post("/", response_model=LicenseEntity)
async def create_license_route(
    *, item_in: LicenseCreate
) -> str:
    """
    Create new license.
    """
    partner = await create_license(item_in)
    return partner


@router.get("/", response_model=List[LicenseEntity])
async def get_all_licenses_route():
    licenses: MutableSequence[LicenseEntity] = await get_all_licenses()
    return licenses


@router.get("/{id}", response_model=LicenseEntity)
async def get_license_route(id: UUID):
    license: LicenseEntity = await get_license(id=id)
    return license


@router.put("/{id}", response_model=LicenseEntity)
async def update_license_route(
    id: UUID, item_in: LicenseUpdate
):
    license: LicenseEntity = await update_license(
        id=id, license_data=item_in
    )
    return license


@router.delete("/{id}", response_model=LicenseEntity)
async def delete_license_route(id: UUID):
    license: LicenseEntity = await delete_license(id=id)
    return license
