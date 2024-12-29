from uuid import UUID
from datetime import datetime
from loguru import logger
from sqlalchemy.sql import func

from ..infra.database import db_session
from ..infra.database.models import (
    Goods as GoodsORM, Seller as SellerORM
)


from .entities.goods import Goods, GoodsCreate


class GoodsViews:

    def __init__(self):
        pass

    def some(self):
        pass


class GoodsQueries:

    def __init__(self):
        pass

    async def get_all_goods(self):
        return GoodsORM.query.all()

    async def get_goods(self, id: UUID):
        return GoodsORM.query.get(id)


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

    def update_goods(self):
        pass

    def delete_goods(self):
        pass

    async def list_count_group_by_name(self) -> list:
        result = db_session.query(
            GoodsORM.name, func.count(GoodsORM.id).label("count")
        ).group_by(GoodsORM.name).all()
        return result
    
    async def list_summ_group_by_name(self) -> list:
        result = db_session.query(
            GoodsORM.name, func.sum(
                GoodsORM.price_after_vat
            ).label("summ")
        ).group_by(GoodsORM.name).all()
        logger.info(f"result[:5] = {result[:5]}")
        return result

    async def goods_by_name_group_by_sellers(
        self, name: str
    ) -> list:
        result = GoodsORM.query.filter_by(
            name=name
        ).join(SellerORM).group_by(seller_id)
        return result
