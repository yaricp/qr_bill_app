from uuid import UUID
from typing import Optional, List

from pydantic import BaseModel

from .login_link import LoginLink


# Shared properties
class UserBase(BaseModel):
    id: Optional[UUID] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = False
    phone: Optional[str] = None
    login: Optional[str] = None
    tg_name: Optional[str] = None
    tg_verified: Optional[bool] = False
    tg_id: Optional[int] = None
    lang: Optional[str] = None
    password: Optional[str] = None


class UserCreate(BaseModel):
    login: str
    password: str


# Properties to receive on item update
class UserUpdate(UserBase):
    id: UUID


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: UUID
    lang: str
    links: Optional[List[LoginLink]] = []

    class Config:
        orm_mode = True


# Properties to return to client
class User(UserInDBBase):
    pass


# Properties properties stored in DB
class UserInDB(UserInDBBase):
    pass
