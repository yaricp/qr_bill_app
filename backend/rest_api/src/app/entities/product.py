from uuid import UUID
from typing import Optional

from pydantic import BaseModel


# Shared properties
class ProductBase(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None


class ProductCreate(BaseModel):
    name: str


# Properties to receive on item update
class ProductUpdate(ProductBase):
    id: UUID


# Properties shared by models stored in DB
class ProductInDBBase(ProductBase):
    id: UUID
    name: str

    class Config:
        orm_mode = True


# Properties to return to client
class Product(ProductInDBBase):
    pass


# Properties properties stored in DB
class ProductInDB(ProductInDBBase):
    pass


class CategoryProduct(BaseModel):
    product_id: UUID
    cat_id: UUID
