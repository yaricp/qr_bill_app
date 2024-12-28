from uuid import UUID
from typing import Optional

from pydantic import BaseModel


# Shared properties
class UnitBase(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None


class UnitCreate(BaseModel):
    name: str


# Properties to receive on item update
class UnitUpdate(UnitBase):
    id: UUID


# Properties shared by models stored in DB
class UnitInDBBase(UnitBase):
    id: UUID
    name: str

    class Config:
        orm_mode = True


# Properties to return to client
class Unit(UnitInDBBase):
    pass


# Properties properties stored in DB
class UnitInDB(UnitInDBBase):
    pass
