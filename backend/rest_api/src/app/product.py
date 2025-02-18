from uuid import UUID
from typing import List
from sqlalchemy.sql import text
from sqlalchemy.sql import func
from sqlalchemy import desc
from loguru import logger

from ..infra.database import db_session
from ..infra.database.models import (
    Bill as BillORM,
    Goods as GoodsORM,
    Seller as SellerORM,
    Product as ProductORM, 
    Category as CategoryORM,
    UserProduct as UserProductORM
)

from .entities.product import (
    Product, ProductCreate, ProductUpdate,
    ProductPrice
)
from .entities.user_product import (
    UserProductCreate, UncategorizedUserProduct,
    CategorizedUserProduct, UserProduct
)

from .utils import unification_names


class ProductQueries:

    def __init__(self):
        pass

    async def get_all_products(self) -> List[Product]:
        return ProductORM.query.all()

    async def get_products_more_one_prices(
        self, user_id: UUID
    ) -> List[Product]:
        result = db_session.query(
            ProductORM.id,
            ProductORM.name
        ).join(
            GoodsORM.user_product
        ).join(
            UserProductORM.product
        ).where(
            GoodsORM.user_id == user_id
        ).group_by(
            ProductORM.id,
            ProductORM.name
        ).order_by(desc(func.count(GoodsORM.id))).having(
           func.count(GoodsORM.id) > 2
        ).all()
        logger.info(f"result: {result}")
        return result

    async def get_user_product(self, id: UUID) -> UserProduct:
        return UserProductORM.query.get(id)

    async def get_uncategorized_product(
        self, user_id: UUID, cat_id: UUID | None = None
    ) -> List[UncategorizedUserProduct]:
        logger.info(f"user_id: {user_id}")
        logger.info(f"cat_id: {cat_id}")
        sql_queries = {
            "cat": "SELECT user_product.id, product.name "\
                " FROM user_product "\
                " JOIN product ON user_product.product_id = product.id "\
                " LEFT JOIN user_product_category "\
                " ON user_product_category.user_product_id = user_product.id "\
                " LEFT JOIN category ON "\
                " user_product_category.cat_id = category.id "\
                f" WHERE user_product.user_id = '{user_id}' "\
                " GROUP BY user_product.id, product.name "\
                " HAVING SUM("\
                f" CASE WHEN category.id != '{cat_id}' THEN 0 ELSE 1 END"\
                ") = 0; ",
            "no_cat": "SELECT user_product.id, product.name "\
                " FROM user_product"\
                " JOIN product ON user_product.product_id = product.id"\
                " LEFT JOIN user_product_category "\
                " ON user_product_category.user_product_id = user_product.id"\
                " LEFT JOIN category "\
                " ON user_product_category.cat_id = category.id"\
                f" WHERE user_product.user_id = '{user_id}'"\
                " GROUP BY user_product.id, product.name"\
                " HAVING COUNT(category.id) = 0;"
        }
        result = []
        if cat_id:
            result = db_session.execute(
                text(sql_queries["cat"])
            )
        else:
            result = db_session.execute(
                text(sql_queries["no_cat"])
            )

        logger.info(f"result: {result}")

        return result

    async def get_product_prices(
        self, product_id: UUID, user_id: UUID
    ) -> List[ProductPrice]:
        result = db_session.query(
            BillORM.created,
            GoodsORM.unit_price_after_vat.label("price"),
            SellerORM.official_name.label("seller"),
            SellerORM.address,
            GoodsORM.name,
            GoodsORM.quantity
        ).join(
            GoodsORM.user_product
        ).join(
            UserProductORM.product
        ).join(
            GoodsORM.seller
        ).join(
            GoodsORM.bill
        ).where(
            ProductORM.id == product_id,
            BillORM.user_id == user_id,
            UserProductORM.user_id == user_id
        ).order_by(
            BillORM.created
        ).all()
        # logger.info(f"result: {result}")
        return result


class ProductCommands:

    def __init__(self):
        self.queries = ProductQueries()

    async def get_by_product_name(
        self, incoming_item: ProductCreate
    ) -> Product:
        prod = ProductORM.query.filter(
            ProductORM.name == incoming_item.name
        ).first()
        logger.info(f"prod: {prod}")
        return prod

    async def get_or_create_product(
        self, incoming_item: ProductCreate
    ) -> Product:
        prod = await self.get_by_product_name(
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

    async def get_or_create_user_product(
        self, incoming_item: ProductCreate, user_id: UUID
    ) -> Product:
        logger.info(f"incoming_item: {incoming_item}")
        product = await self.get_or_create_product(incoming_item=incoming_item)
        exists_user_prod = UserProductORM.query.filter(
            UserProductORM.user_id == user_id,
            UserProductORM.product_id == product.id
        ).all()
        if exists_user_prod:
            return exists_user_prod[0]
        user_prod_data = UserProductCreate(
            user_id=user_id,
            product_id=product.id
        )
        user_prod = UserProductORM(**user_prod_data.dict())
        db_session.add(user_prod)
        db_session.commit()
        logger.info(f"user_prod: {user_prod}")
        return user_prod

    async def update_product(
        self, incoming_item: ProductUpdate
    ) -> Product:
        pass

    async def save_categorized_products(
        self,
        cat_prod_data: List[CategorizedUserProduct],
    ) -> bool:
        logger.info(f"cat_prod_data: {cat_prod_data}")
        try:
            for item in cat_prod_data:
                user_product = await self.queries.get_user_product(
                    item.user_product_id
                )
                cat = CategoryORM.query.get(item.cat_id)
                logger.info(f"cat: {cat}")
                user_product.categories.add(cat)
                db_session.commit()
            return True
        except Exception as err:
            logger.error(f"Error: {err}")
            return False
        return True

    async def update_product_categories(
        self,
        user_product_id: UUID,
        list_cat_id: List[UUID]
    ) -> bool:
        user_product = UserProductORM.query.get(user_product_id)
        list_for_remove = [old_cat for old_cat in user_product.categories]
        for old_cat in list_for_remove:
            user_product.categories.remove(old_cat)
        for cat_id in list_cat_id:
            new_cat = CategoryORM.query.get(cat_id)
            user_product.categories.add(new_cat)
        try:
            db_session.add(user_product)
            db_session.commit()
        except Exception as err:
            logger.error(f"Error: {err}")
            return False
        return True

    async def delete_product(self, id:UUID) -> Product:
        pass

    async def normalize_products_name(self) -> bool:
        for product in ProductORM.query.all():
            try:
                product.name = unification_names(product.name)
                db_session.commit()
            except Exception as err:
                logger.info(f"Error: {err}")
                return False
        return True
