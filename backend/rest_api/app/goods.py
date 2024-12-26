from uuid import UUID
from datetime import datetime
from loguru import logger

from ..infra.database import db_session
from ..infra.database.models import Goods as GoodsORM

from .entities.goods import Goods, GoodsCreate


class GoodsViews:

    def __init__(self):
        pass

    def some(self):
        pass


class GoodsQueries:

    def __init__(self):
        pass

    def get_all_goods(self):
        pass

    def get_goods(self):
        pass


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
