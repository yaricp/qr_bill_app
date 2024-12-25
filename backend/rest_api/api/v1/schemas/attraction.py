from uuid import UUID
from typing import Optional

from pydantic import BaseModel


# Shared properties
class AttractionBase(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    location: Optional[str] = None
    partner_id: Optional[UUID] = None


class AttractionCreate(BaseModel):
    name: str
    location: str
    partner_id: UUID


# Properties to receive on item update
class AttractionUpdate(BaseModel):
    id: UUID
    name: str
    location: str
    partner_id: UUID


# Properties shared by models stored in DB
class AttractionInDBBase(AttractionBase):
    id: UUID
    name: str
    owner_id: UUID
    meshfile: str

    class Config:
        orm_mode = True


# Properties to return to client
class Attraction(AttractionInDBBase):
    pass


# Properties properties stored in DB
class AttractionInDB(AttractionInDBBase):
    pass
