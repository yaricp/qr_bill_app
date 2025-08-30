from uuid import UUID
from typing import List
from loguru import logger
from sqlalchemy.sql import func
from sqlalchemy import desc

from ..infra.database import db_session
from ..infra.database.models import (
    Bill as BillORM,
    Goods as GoodsORM,
    Seller as SellerORM
)
# from ..infra.database.models.seller import Seller as SellerORM
# from ..infra.database.models.user_product import UserProduct as UserProductORM
# from ..infra.database.models.bill import Bill as BillORM
# from ..infra.database.models.goods import Goods as GoodsORM

from .entities.seller import (
    Seller, SellerCreate, CountBillsByNameSeller,
    CountGoodsByNameSeller, SummBillsByNameSeller
)
from .metrics.analytics import metric_analytics


class SellerViews:

    def __init__(self):
        pass

    def some(self):
        pass


class SellerQueries:

    def __init__(self):
        pass

    async def get_all_sellers(
        self, user_id: UUID, offset: int = 0, limit: int = 0
    ) -> Seller:
        if offset > 0 and limit > 0:
            return SellerORM.query.join(BillORM).filter_by(
                user_id=user_id
            ).offset(offset).limit(limit).all()
        elif limit > 0:
            return SellerORM.query.join(BillORM).filter_by(
                user_id=user_id
            ).limit(limit).all()
        elif offset > 0:
            return SellerORM.query.join(BillORM).filter_by(
                user_id=user_id
            ).offset(offset).all()
        return SellerORM.query.join(BillORM).filter_by(user_id=user_id).all()

    async def get_seller(self, id: UUID):
        return SellerORM.query.get(id)

    @metric_analytics
    async def get_sellers_order_by_count_goods(
        self, first_of: int, user_id: UUID
    ) -> List[CountGoodsByNameSeller]:
        if first_of:
            result = db_session.query(
                SellerORM.name,
                func.sum(GoodsORM.quantity).label("count")
            ).join(SellerORM.goods_list).filter(
                GoodsORM.user_id == user_id
            ).group_by(
                SellerORM.name
            ).order_by(desc("count")).limit(first_of)
        else:
            result = db_session.query(
                SellerORM.name,
                func.sum(GoodsORM.quantity).label("count")
            ).join(SellerORM.goods_list).filter(
                GoodsORM.user_id == user_id
            ).group_by(
                SellerORM.name
            ).order_by(desc("count")).all()
        return result

    @metric_analytics
    async def get_sellers_order_by_count_bills(
        self, first_of: int, user_id: UUID
    ) -> List[CountBillsByNameSeller]:
        logger.info(f"user_id: {user_id}")
        if first_of:
            result = db_session.query(
                SellerORM.official_name.label("name"),
                func.count(BillORM.id).label("count")
            ).where(
                BillORM.user_id == user_id
            ).join(SellerORM).group_by(
                SellerORM.official_name
            ).order_by(desc("count")).limit(first_of)
        else:
            result = db_session.query(
                SellerORM.official_name.label("name"),
                func.count(BillORM.id).label("count")
            ).where(
                BillORM.user_id == user_id
            ).join(SellerORM).group_by(
                SellerORM.official_name
            ).order_by(desc("count")).all()
        return result

    @metric_analytics
    async def get_sellers_order_by_summ_bills(
        self, first_of: int, user_id: UUID
    ) -> List[SummBillsByNameSeller]:
        if first_of:
            result = db_session.query(
                SellerORM.official_name.label("name"),
                func.sum(BillORM.value).label("summ")
            ).where(
                BillORM.user_id == user_id
            ).join(SellerORM).group_by(
                SellerORM.official_name
            ).order_by(desc("summ")).limit(first_of)
        else:
            result = db_session.query(
                SellerORM.official_name.label("name"),
                func.sum(BillORM.value).label("summ")
            ).where(
                BillORM.user_id == user_id
            ).join(SellerORM).group_by(
                SellerORM.official_name
            ).order_by(desc("summ")).all()

        return result


class SellerCommands:

    def __init__(self):
        pass

    async def get_by_name_address(self, incoming_item: SellerCreate) -> Seller:
        seller = SellerORM.query.filter(
            SellerORM.official_name == incoming_item.official_name,
            SellerORM.address == incoming_item.address
        ).first()
        logger.info(f"seller: {seller}")
        return seller

    async def get_or_create(self, incoming_item: SellerCreate) -> Seller:
        seller = await self.get_by_name_address(
            incoming_item=incoming_item
        )
        if not seller:
            seller = await self.create_seller(
                incoming_item=incoming_item
            )
        return seller

    async def create_seller(self, incoming_item: SellerCreate) -> Seller:
        logger.info(f"incoming_item: {incoming_item}")
        incoming_item_dict = incoming_item.dict()
        name_exists = False
        logger.info(f"incoming_item_dict: {incoming_item_dict}")
        if "name" in incoming_item_dict and incoming_item_dict["name"]:
            name_exists = True
        if not name_exists:
            if len(incoming_item.official_name) > 5:
                incoming_item_dict["name"] = incoming_item.official_name[:5]
            else:
                incoming_item_dict["name"] = incoming_item.official_name
        logger.info(
            f"incoming_item_dict[name]: {incoming_item_dict['name']}"
        )
        seller = SellerORM(**incoming_item_dict)
        db_session.add(seller)
        db_session.commit()
        logger.info(f"seller: {seller}")
        return seller

    def update_seller(self):
        pass

    def delete_seller(self, id: UUID):
        pass
