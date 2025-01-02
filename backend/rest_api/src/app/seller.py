from uuid import UUID
from loguru import logger
from sqlalchemy.sql import func
from sqlalchemy import desc

from ..infra.database import db_session
from ..infra.database.models.seller import Seller as SellerORM

from .entities.seller import Seller, SellerCreate


class SellerViews:

    def __init__(self):
        pass

    def some(self):
        pass


class SellerQueries:

    def __init__(self):
        pass

    async def get_all_sellers(self):
        return SellerORM.query.all()

    async def get_seller(self, id: UUID):
        return SellerORM.query.get(id)

    async def get_sellers_order_by_count_goods(self):
        return db_session.query(
            SellerORM.name, func.count(SellerORM.goods).label("count_goods")
        ).group_by(SellerORM.name).order_by(desc("count_goods")).all()

    async def get_sellers_order_by_count_bills(self):
        return db_session.query(
            SellerORM.name, func.count(SellerORM.bills).label("count_bills")
        ).group_by(SellerORM.name).order_by(desc("count_bills")).all()

    async def get_sellers_order_by_summ_bills(self):
        return db_session.query(
            SellerORM.name, func.sum(SellerORM.bills).label("summ_bills")
        ).group_by(SellerORM.name).order_by(desc("summ_bills")).all()


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
