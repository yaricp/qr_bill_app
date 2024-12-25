from uuid import UUID
from typing import Optional

from pydantic import BaseModel

from ....domain.value_objects.license_status import LicenseStatus
from ....domain.value_objects.license_type import LicenseType


# Shared properties
class LicenseBase(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    type: Optional[LicenseType] = None
    status: Optional[LicenseStatus] = None
    count_packages: Optional[int] = None
    # datetime_expiration: Optional[datetime] = None
    attraction_id: Optional[UUID] = None


class LicenseCreate(BaseModel):
    name: str
    description: str
    type: LicenseType
    partner_id: UUID
    count_packages: int
    # datetime_expiration: Optional[datetime]


class LicenseUpdate(BaseModel):
    id: UUID
    name: str
    description: str
    attraction_id: Optional[UUID] = None
