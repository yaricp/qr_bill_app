from uuid import UUID
from typing import List
from datetime import datetime
from loguru import logger
from sqlalchemy.sql import func
from sqlalchemy import desc

from ..infra.database import db_session
from ..infra.database.models.base import association_goods_category
from ..infra.database.models import (
    Goods as GoodsORM, Seller as SellerORM,
    Category as CategoryORM
)


from .entities.goods import (
    Goods, GoodsCreate, GoodsUpdate, CategoryGoods
)


class GoodsViews:

    def __init__(self):
        pass

    def some(self):
        pass


class GoodsQueries:

    def __init__(self):
        pass

    async def get_all_goods(self, user_id: UUID):
        return GoodsORM.query.filter_by(user_id=user_id).all()

    async def get_goods(self, id: UUID):
        return GoodsORM.query.get(id)

    async def list_count_group_by_name(
        self, user_id: UUID, first_of: int = 0
    ) -> list:
        logger.info(f"first_of: {first_of}")
        if first_of:
            result = db_session.query(
                GoodsORM.name, func.sum(GoodsORM.quantity).label("count")
            ).where(GoodsORM.user_id == user_id).group_by(
                GoodsORM.name
            ).order_by(desc("count")).limit(first_of)
        else:
            result = db_session.query(
                GoodsORM.name, func.sum(GoodsORM.quantity).label("count")
            ).where(GoodsORM.user_id == user_id).group_by(
                GoodsORM.name
            ).order_by(desc("count")).all()
        return result

    async def list_summ_group_by_name(
        self, user_id: UUID, first_of: int = 0
    ) -> list:
        if first_of:
            result = db_session.query(
                GoodsORM.name,
                func.sum(GoodsORM.price_after_vat).label("summ")
            ).where(GoodsORM.user_id == user_id).group_by(
                GoodsORM.name
            ).order_by(desc("summ")).limit(first_of)
        else:
            result = db_session.query(
                GoodsORM.name,
                func.sum(GoodsORM.price_after_vat).label("summ")
            ).where(GoodsORM.user_id == user_id).group_by(
                GoodsORM.name
            ).order_by(desc("summ")).all()
        logger.info(f"result[:5] = {result[:5]}")
        return result

    async def goods_by_name_group_by_sellers(
        self, name: str, user_id: UUID
    ) -> list:
        result = GoodsORM.query(
            SellerORM.name,
            func.sum(GoodsORM.quantity).label("count")
        ).join(SellerORM).where(
            GoodsORM.user_id == user_id,
            GoodsORM.name == name
        ).group_by(
            SellerORM.name
        ).order_by(desc("count")).all()
        return result

    async def list_uncategorized_goods(
        self, user_id: UUID, cat_id: UUID | None = None
    ) -> List[Goods]:
        result = []
        user_goods = GoodsORM.query.filter_by(
            user_id=user_id
        ).all()
        for u_goods in user_goods:
            if cat_id:
                if cat_id not in [item.id for item in u_goods.categories]:
                    result.append(u_goods)
            else:
                logger.info(f"u_goods.categories: {u_goods.categories}")
                if not u_goods.categories:
                    logger.info(f"added: {u_goods}")
                    result.append(u_goods)

        return result


class GoodsCommands:

    def __init__(self):
        pass

    async def get_by_name_bill_id(self, incoming_item: GoodsCreate) -> Goods:
        goods = GoodsORM.query.filter(
            GoodsORM.name == incoming_item.name,
            GoodsORM.bill_id == incoming_item.bill_id
        ).first()
        logger.info(f"goods: {goods}")
        return goods

    async def get_or_create(self, incoming_item: GoodsCreate) -> Goods:
        goods = await self.get_by_name_bill_id(
            incoming_item=incoming_item
        )
        if not goods:
            goods = await self.create_goods(
                incoming_item=incoming_item
            )
        return goods

    async def create_goods(self, incoming_item: GoodsCreate) -> Goods:
        logger.info(f"incoming_item: {incoming_item}")
        incoming_item_dict = incoming_item.dict()
        goods = GoodsORM(**incoming_item_dict)
        db_session.add(goods)
        db_session.commit()
        logger.info(f"goods: {goods}")
        return goods

    async def update_goods_categories(
        self, goods_id: UUID, goods_data: List[CategoryGoods]
    ) -> bool:
        goods = GoodsORM.query.get(goods_id)
        list_for_remove = [old_cat for old_cat in goods.categories]
        for old_cat in list_for_remove:
            goods.categories.remove(old_cat)
        for item in goods_data:
            new_cat = CategoryORM.query.get(item.cat_id)
            goods.categories.add(new_cat)
        try:
            db_session.add(goods)
            db_session.commit()
        except Exception as err:
            logger.error(f"Error: {err}")
            return False
        return True

    async def save_categorized_goods(
        self, goods_data: List[CategoryGoods]
    ) -> bool:
        logger.info(f"goods_data: {goods_data}")
        try:
            for item in goods_data:
                goods = GoodsORM.query.get(item.goods_id)
                cat = CategoryORM.query.get(item.cat_id)
                logger.info(f"cat: {cat}")
                goods.categories.add(cat)
                db_session.commit()
            return True
        except Exception as err:
            logger.error(f"Error: {err}")
            return False
        return True

    async def update_goods(self, incoming_item: GoodsUpdate) -> Goods:
        found_goods = GoodsORM.query.get(incoming_item.id)
        incoming_item_dict = incoming_item.dict()
        for key, value in incoming_item_dict.items():
            if value != None:
                setattr(found_goods, key, value)
        db_session.commit()
        return found_goods

    async def delete_goods(self, user_id: UUID):
        pass

    async def strip_all_names(self) -> bool:
        for goods in GoodsORM.query.all():
            new_goods = GoodsUpdate(
                id=goods.id,
                name=goods.name.strip()
            )
            await self.update_goods(incoming_item=new_goods)
        return True
