from uuid import UUID
from typing import Optional

from pydantic import BaseModel


# Shared properties
class PartnerBase(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class PartnerCreate(BaseModel):
    name: str
    address: str
    email: str
    phone: str


# Properties to receive on item update
class PartnerUpdate(PartnerBase):
    id: UUID


# Properties shared by models stored in DB
class PartnerInDBBase(PartnerBase):
    id: UUID
    name: str
    owner_id: UUID
    meshfile: str

    class Config:
        orm_mode = True


# Properties to return to client
class Partner(PartnerInDBBase):
    pass


# Properties properties stored in DB
class PartnerInDB(PartnerInDBBase):
    pass
