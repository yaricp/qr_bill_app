from typing import List
from uuid import UUID

from pydantic import BaseModel

from .category import Category
from .product import Product


class UncategorizedUserProduct(BaseModel):
    id: UUID
    name: str


class UserProduct(BaseModel):
    id: UUID
    product: Product
    categories: List[Category]


class CategorizedProduct(BaseModel):
    user_product_id: UUID
    cat_id: UUID


class UpdateUserProductCategories(BaseModel):
    user_product_id: UUID
    list_cat_id: List[UUID]
