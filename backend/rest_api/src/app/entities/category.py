from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from .product import Product


# Shared properties
class CategoryBase(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    user_id: Optional[UUID] = None


class CategoryCreate(BaseModel):
    name: str
    user_id: UUID


# Properties to receive on item update
class CategoryUpdate(CategoryBase):
    id: UUID


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: UUID
    name: str
    products: List[Product]
    user_id: UUID

    class Config:
        orm_mode = True


# Properties to return to client
class Category(CategoryInDBBase):
    pass


# Properties properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass
