from uuid import UUID
from typing import List
from datetime import datetime, timedelta
from sqlalchemy.sql import func
from sqlalchemy import desc
from loguru import logger

from ..infra.database import db_session
from ..infra.database.models import (
    Product as ProductORM, Category as CategoryORM
)

from .entities.product import (
    Product, ProductCreate, ProductUpdate
)
from .entities.product import CategoryProduct


def unification_names(raw_name: str) -> str:
    result = raw_name.strip().lower()
    return f"{result[0].upper()}{result[1:]}"


class ProductQueries:

    def __init__(self):
        pass

    async def get_all_products(self) -> List[Product]:
        return ProductORM.query.all()

    def get_product(self, id: UUID) -> Product:
        return ProductORM.query.get(id)


class ProductCommands:

    def __init__(self):
        pass

    async def get_by_name(
        self, incoming_item: ProductCreate
    ) -> Product:
        prod = ProductORM.query.filter(
            ProductORM.name == incoming_item.name
        ).first()
        logger.info(f"prod: {prod}")
        return prod

    async def get_or_create(
        self, incoming_item: ProductCreate
    ) -> Product:
        prod = await self.get_by_name(
            incoming_item=incoming_item
        )
        if not prod:
            prod = await self.create_product(
                incoming_item=incoming_item
            )
        return prod

    async def create_product(
        self, incoming_item: ProductCreate
    ) -> Product:
        logger.info(f"incoming_item: {incoming_item}")
        incoming_item_dict = incoming_item.dict()
        prod = ProductORM(**incoming_item_dict)
        db_session.add(prod)
        db_session.commit()
        logger.info(f"prod: {prod}")
        return prod

    async def update_product(
        self, incoming_item: ProductUpdate
    ) -> Product:
        pass

    async def save_categorized_product(
        self, product_data: List[CategoryProduct]
    ) -> bool:
        logger.info(f"product_data: {product_data}")
        try:
            for item in product_data:
                product = ProductORM.query.get(item.product_id)
                cat = CategoryORM.query.get(item.cat_id)
                logger.info(f"cat: {cat}")
                product.categories.add(cat)
                db_session.commit()
            return True
        except Exception as err:
            logger.error(f"Error: {err}")
            return False
        return True

    async def update_product_categories(
        self, product_id: UUID, product_data: List[CategoryProduct]
    ) -> bool:
        product = ProductORM.query.get(product_id)
        list_for_remove = [old_cat for old_cat in product.categories]
        for old_cat in list_for_remove:
            product.categories.remove(old_cat)
        for item in product_data:
            new_cat = CategoryORM.query.get(item.cat_id)
            product.categories.add(new_cat)
        try:
            db_session.add(product)
            db_session.commit()
        except Exception as err:
            logger.error(f"Error: {err}")
            return False
        return True

    async def delete_product(self, id:UUID) -> Product:
        pass