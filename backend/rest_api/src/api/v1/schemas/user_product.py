from uuid import UUID
from typing import Optional

from pydantic import BaseModel

from .product import Product


class UncategorizedUserProduct(BaseModel):
    id: UUID
    name: str


class UserProduct(BaseModel):
    product: Product


class CategorizedProduct(BaseModel):
    user_product_id: UUID
    cat_id: UUID
