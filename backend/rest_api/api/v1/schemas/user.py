from uuid import UUID
from typing import Optional

from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[UUID] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    altitude: Optional[float] = None
    meshfile: Optional[str] = None
    picture: Optional[str] = None
    wall_thickness: Optional[float] = None
    heat_accumulator_volume: Optional[float] = None
    check_sum_meshfile: Optional[str] = None


class UserCreate(BaseModel):
    name: str
    meshfile: str
    description: Optional[str] = None


# Properties to receive on item update
class UserUpdate(UserBase):
    id: UUID


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: UUID
    name: str
    owner_id: UUID
    meshfile: str

    class Config:
        orm_mode = True


# Properties to return to client
class User(UserInDBBase):
    pass


# Properties properties stored in DB
class UserInDB(UserInDBBase):
    pass
