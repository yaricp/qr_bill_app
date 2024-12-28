from uuid import UUID
from loguru import logger

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

    def get_all_sellers(self):
        pass

    def get_seller(self):
        pass


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
        if "name" not in incoming_item_dict:
            incoming_item_dict["name"] = incoming_item.official_name[:5]
        seller = SellerORM(**incoming_item_dict)
        db_session.add(seller)
        db_session.commit()
        logger.info(f"seller: {seller}")
        return seller

    def update_seller(self):
        pass

    def delete_seller(self, id: UUID):
        pass
