from uuid import UUID
from typing import Optional, List
from decimal import Decimal

from pydantic import BaseModel

from .user_product import UserProduct


# Shared properties
class CategoryBase(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    user_id: Optional[UUID] = None


class CategoryCreate(CategoryBase):
    name: str


# Properties to receive on item update
class CategoryUpdate(CategoryBase):
    id: UUID


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: UUID
    name: str
    # user_products: List[UserProduct]

    class Config:
        orm_mode = True


# Properties to return to client
class Category(CategoryInDBBase):
    pass


# Properties properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass


class CategoryCountByName(BaseModel):
    name: str
    count: Decimal


class CategorySummByName(BaseModel):
    name: str
    summ: Decimal
