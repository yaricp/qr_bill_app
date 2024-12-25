from uuid import UUID
from typing import Optional

from pydantic import BaseModel


class CategoryBase(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(CategoryBase):
    name: str


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: UUID
    name: str
    address: str

    class Config:
        orm_mode = True


# Properties to return to client
class Category(CategoryInDBBase):
    pass


# Properties properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass
