from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class LoginLinkBase(BaseModel):
    id: Optional[UUID] = None
    link_for: Optional[str] = None
    created: Optional[datetime] = None


# class LoginLinkCreate(BaseModel):
#     name: str


# # Properties to receive on item update
# class LoginLinkUpdate(LoginLinkBase):
#     id: UUID


# Properties shared by models stored in DB
class LoginLinkInDBBase(LoginLinkBase):
    id: UUID
    link_for: str
    created: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class LoginLink(LoginLinkInDBBase):
    pass


# Properties properties stored in DB
class LoginLinkInDB(LoginLinkInDBBase):
    pass
