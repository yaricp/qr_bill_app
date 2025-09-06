from uuid import UUID
from typing import List

from pydantic import BaseModel

from .product import Product
from .category import Category


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
