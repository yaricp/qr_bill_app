from uuid import UUID
from typing import List, Optional
from loguru import logger

from fastapi import Depends

from ... import app, manager
from ...config import URLPathsConfig
from ..services.product import (
    get_product, create_product,
    delete_product, get_all_products, update_product,
    get_uncategorized_product, save_categorized_products,
    update_product_categories, get_product_prices,
    get_products_more_one_prices
)
from ..schemas.product import (
    Product, ProductCreate, ProductUpdate, ProductPrice
)
from ..schemas.user_product import (
    UncategorizedUserProduct, CategorizedProduct,
    UpdateUserProductCategories
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


@app.get(
    URLPathsConfig.PREFIX + "/products/uncategorized/",
    tags=['Products'],
    response_model=List[UncategorizedUserProduct]
)
@app.get(
    URLPathsConfig.PREFIX + "/products/uncategorized/{cat_id}",
    tags=['Products'],
    response_model=List[UncategorizedUserProduct]
)
async def get_uncategorized_product_route(
    cat_id: Optional[UUID] = None, user=Depends(manager)
) -> List[UncategorizedUserProduct]:
    product: List[UncategorizedUserProduct] = await get_uncategorized_product(
        user_id=user.id, cat_id=cat_id
    )
    return product


@app.post(
    URLPathsConfig.PREFIX + "/products/save_categorized/",
    tags=['Products'],
    response_model=bool
)
async def save_categorized_goods_route(
    data_in: List[CategorizedProduct], user=Depends(manager)
) -> bool:
    """
    Assosiate category to several goods.
    """
    result = await save_categorized_products(
        cat_prod_data=data_in
    )
    return result


@app.put(
    URLPathsConfig.PREFIX + "/products/update_categories/",
    tags=['Products'],
    response_model=bool
)
async def update_product_categories_route(
    data_in: UpdateUserProductCategories, user=Depends(manager)
) -> bool:
    """
    Assosiate category to several goods.
    """
    result = await update_product_categories(
        user_product_id=data_in.user_product_id,
        list_cat_id=data_in.list_cat_id
    )
    return result


@app.get(
    URLPathsConfig.PREFIX + "/products/prices/{product_id}",
    tags=['Products'],
    response_model=List[ProductPrice]
)
async def product_prices_route(
    product_id: UUID, user=Depends(manager)
) -> List[ProductPrice]:
    result: List[
        ProductPrice
    ] = await get_product_prices(
        product_id=product_id, user_id=user.id
    )
    return result


@app.get(
    URLPathsConfig.PREFIX + "/products/for_prices/",
    tags=['Products'],
    response_model=List[Product]
)
async def products_for_prices_route(
    user=Depends(manager)
) -> List[Product]:
    result: List[Product] = await get_products_more_one_prices(
        user_id=user.id
    )
    return result


# @app.get(
#     URLPathsConfig.PREFIX + "/products/normalize/",
#     tags=['Products'],
#     response_model=bool
# )
# async def normalize_products_name_route(user=Depends(manager)) -> bool:
#     result = await normalize_products_name()
#     return result
