from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class LoginLinkBase(BaseModel):
    id: Optional[UUID] = None
    link_for: Optional[str] = None
    created: Optional[datetime] = None


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
