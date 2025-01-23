from uuid import UUID
from typing import List
from loguru import logger

from fastapi import Depends

from ... import app, manager
from ...config import URLPathsConfig
from ..services.product import (
    get_product, create_product,
    update_product, delete_product, get_all_products
)
from ..schemas.product import (
    Product, ProductCreate, ProductUpdate
)


@app.post(
    URLPathsConfig.PREFIX + "/products/",
    tags=['Products'],
    response_model=Product
)
async def create_product_route(
    item_in: ProductCreate, user=Depends(manager)
) -> Product:
    """
    Create new product.
    """
    product = await create_product(item_in)
    return product


@app.get(
    URLPathsConfig.PREFIX + "/products/",
    tags=['Products'],
    response_model=List[Product]
)
async def get_all_products_route(user=Depends(manager)):
    products: List[Product] = await get_all_products()
    return products


@app.get(
    URLPathsConfig.PREFIX + "/products/{id}",
    tags=['Products'],
    response_model=Product
)
async def get_product_route(id: UUID, user=Depends(manager)):
    product: Product = await get_product(id=id)
    return product


@app.put(
    URLPathsConfig.PREFIX + "/products/{id}",
    tags=['Products'],
    response_model=Product
)
async def update_product_route(
    id: UUID, item_in: ProductUpdate, user=Depends(manager)
):
    product: Product = await update_product(
        id=id, product_data=item_in
    )
    return product


@app.delete(
    URLPathsConfig.PREFIX + "/products/{id}",
    tags=['Products'],
    response_model=Product
)
async def delete_product_route(id: UUID, user=Depends(manager)):
    product: Product = await delete_product(id=id)
    return product
