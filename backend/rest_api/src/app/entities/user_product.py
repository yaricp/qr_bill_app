from uuid import UUID
from typing import Optional

from pydantic import BaseModel

from .product import Product


# Shared properties
class UserProductBase(BaseModel):
    id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    product_id: Optional[UUID] = None


class UserProductCreate(BaseModel):
    user_id: UUID
    product_id: UUID


class ProductInDBBase(UserProductBase):
    id: UUID
    product: Product

    class Config:
        orm_mode = True


# Properties to return to client
class UserProduct(ProductInDBBase):
    pass


# Properties properties stored in DB
class UserProductInDB(ProductInDBBase):
    pass


class CategorizedUserProduct(BaseModel):
    user_product_id: UUID
    cat_id: UUID


class UncategorizedUserProduct(BaseModel):
    id: UUID
    name: str
