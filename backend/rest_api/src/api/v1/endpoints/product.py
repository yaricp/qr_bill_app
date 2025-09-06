from uuid import UUID
from typing import List, Optional

from fastapi import Depends, HTTPException

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
    tags=["Products"],
    response_model=Product
)
async def create_product_route(
    item_in: ProductCreate, user=Depends(manager)
) -> Product:
    """ Creates a new product """
    return await create_product(item_in)


@app.get(
    URLPathsConfig.PREFIX + "/products/",
    tags=["Products"],
    response_model=List[Product]
)
async def get_all_products_route(user=Depends(manager)) -> List[Product]:
    """ Shows list of products """
    return await get_all_products()


@app.get(
    URLPathsConfig.PREFIX + "/products/{id}",
    tags=["Products"],
    response_model=Product
)
async def get_product_route(id: UUID, user=Depends(manager)) -> Product:
    """ Shows product info """
    product: Product = await get_product(id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put(
    URLPathsConfig.PREFIX + "/products/{id}",
    tags=["Products"],
    response_model=Product
)
async def update_product_route(
    id: UUID, item_in: ProductUpdate, user=Depends(manager)
) -> Product:
    """ Updates product info """
    product: Product = await update_product(
        id=id, product_data=item_in
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.delete(
    URLPathsConfig.PREFIX + "/products/{id}",
    tags=["Products"],
    response_model=Product
)
async def delete_product_route(id: UUID, user=Depends(manager)) -> Product:
    """ Deletes product """
    product: Product = await delete_product(id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get(
    URLPathsConfig.PREFIX + "/products/uncategorized/",
    tags=["Products"],
    response_model=List[UncategorizedUserProduct]
)
@app.get(
    URLPathsConfig.PREFIX + "/products/uncategorized/{cat_id}",
    tags=["Products"],
    response_model=List[UncategorizedUserProduct]
)
async def get_uncategorized_product_route(
    cat_id: Optional[UUID] = None, user=Depends(manager)
) -> List[UncategorizedUserProduct]:
    """ Shows products not assigned to category """
    return await get_uncategorized_product(
        user_id=user.id, cat_id=cat_id
    )


@app.post(
    URLPathsConfig.PREFIX + "/products/save_categorized/",
    tags=["Products"],
    response_model=bool
)
async def save_categorized_goods_route(
    data_in: List[CategorizedProduct], user=Depends(manager)
) -> bool:
    """
    Assigns category to several goods.
    """
    return await save_categorized_products(
        cat_prod_data=data_in
    )


@app.put(
    URLPathsConfig.PREFIX + "/products/update_categories/",
    tags=["Products"],
    response_model=bool
)
async def update_product_categories_route(
    data_in: UpdateUserProductCategories, user=Depends(manager)
) -> bool:
    """
    Assosiates category to several goods.
    """
    return await update_product_categories(
        user_product_id=data_in.user_product_id,
        list_cat_id=data_in.list_cat_id
    )


@app.get(
    URLPathsConfig.PREFIX + "/products/prices/{product_id}",
    tags=["Products"],
    response_model=List[ProductPrice]
)
async def product_prices_route(
    product_id: UUID, user=Depends(manager)
) -> List[ProductPrice]:
    """ Gets price of a product """
    return await get_product_prices(
        product_id=product_id, user_id=user.id
    )


@app.get(
    URLPathsConfig.PREFIX + "/products/for_prices/",
    tags=["Products"],
    response_model=List[Product]
)
async def products_for_prices_route(
    user=Depends(manager)
) -> List[Product]:
    """ Gets products that have more than one price """
    return await get_products_more_one_prices(
        user_id=user.id
    )
