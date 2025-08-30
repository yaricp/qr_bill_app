from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy.sql import func
from sqlalchemy import desc
from loguru import logger

from ..utils import (
    get_last_day_of_month_by_datetime,
    get_fisrt_day_month_by_delta_month
)
from ..infra.database import db_session
from ..infra.database.models import (
    Bill as BillORM,
    Goods as GoodsORM,
    Category as CategoryORM,
    UserProduct as UserProductORM
)

from .entities.category import (
    Category, CategoryCreate, CategoryUpdate
)
from .metrics.analytics import metric_analytics


class CategoryQueries:

    def __init__(self):
        pass

    async def get_all_categories(self, user_id: UUID):
        return CategoryORM.query.filter_by(
            user_id=user_id
        ).all()

    async def get_category(self, id: UUID, user_id: UUID):
        return CategoryORM.query.filter_by(
            id=id,
            user_id=user_id
        ).first()

    @metric_analytics
    async def count_goods_by_name(
        self, first_of: int, user_id: UUID, delta_month: int = -1
    ):
        logger.info(f"first_of: {first_of}")
        logger.info(f"delta_month: {delta_month}")
        if first_of:
            if delta_month != 1:
                prev_month_date = get_fisrt_day_month_by_delta_month(
                    delta_month
                )
                logger.info(f"prev_month_date: {prev_month_date}")
                next_month_date = get_last_day_of_month_by_datetime(
                    prev_month_date
                )
                logger.info(f"next_month_date: {next_month_date}")

                result = db_session.query(
                    CategoryORM.name,
                    func.sum(GoodsORM.quantity).label("count")
                ).join(
                    GoodsORM.bill
                ).join(
                    GoodsORM.user_product
                ).join(
                    UserProductORM.categories
                ).filter(
                    CategoryORM.user_id == user_id,
                    GoodsORM.user_id == user_id,
                    BillORM.created >= prev_month_date,
                    BillORM.created <= next_month_date
                ).group_by(
                    CategoryORM.name
                ).order_by(desc("count")).limit(first_of)
            else:
                result = db_session.query(
                    CategoryORM.name,
                    func.sum(GoodsORM.quantity).label("count")
                ).join(
                    GoodsORM.bill
                ).join(
                    GoodsORM.user_product
                ).join(
                    UserProductORM.categories
                ).filter(
                    CategoryORM.user_id == user_id,
                    GoodsORM.user_id == user_id
                ).group_by(
                    CategoryORM.name
                ).order_by(desc("count")).limit(first_of)
        else:
            if delta_month != 1:
                prev_month_date = get_fisrt_day_month_by_delta_month(
                    delta_month
                )
                logger.info(f"prev_month_date: {prev_month_date}")
                next_month_date = get_last_day_of_month_by_datetime(
                    prev_month_date
                )
                logger.info(f"next_month_date: {next_month_date}")
                result = db_session.query(
                    CategoryORM.name,
                    func.sum(GoodsORM.quantity).label("count")
                ).join(
                    GoodsORM.bill
                ).join(
                    GoodsORM.user_product
                ).join(
                    UserProductORM.categories
                ).filter(
                    CategoryORM.user_id == user_id,
                    GoodsORM.user_id == user_id,
                    BillORM.created >= prev_month_date,
                    BillORM.created <= next_month_date
                ).group_by(
                    CategoryORM.name
                ).order_by(desc("count")).all()
            else:
                result = db_session.query(
                    CategoryORM.name,
                    func.sum(GoodsORM.quantity).label("count")
                ).join(
                    GoodsORM.bill
                ).join(
                    GoodsORM.user_product
                ).join(
                    UserProductORM.categories
                ).filter(
                    CategoryORM.user_id == user_id,
                    GoodsORM.user_id == user_id
                ).group_by(
                    CategoryORM.name
                ).order_by(desc("count")).all()

        return result

    @metric_analytics
    async def summ_goods_by_name(
        self, first_of: int, user_id: UUID, delta_month: int = -1
    ):
        logger.info(f"first_of: {first_of}")
        logger.info(f"delta_month: {delta_month}")
        if first_of:
            if delta_month != 1:
                prev_month_date = get_fisrt_day_month_by_delta_month(
                    delta_month
                )
                logger.info(f"prev_month_date: {prev_month_date}")
                next_month_date = get_last_day_of_month_by_datetime(
                    prev_month_date
                )
                logger.info(f"next_month_date: {next_month_date}")
                result = db_session.query(
                    CategoryORM.name,
                    func.sum(GoodsORM.price_after_vat).label("summ")
                ).join(
                    GoodsORM.bill
                ).join(
                    GoodsORM.user_product
                ).join(
                    UserProductORM.categories
                ).filter(
                    CategoryORM.user_id == user_id,
                    GoodsORM.user_id == user_id,
                    BillORM.created >= prev_month_date,
                    BillORM.created <= next_month_date
                ).group_by(
                    CategoryORM.name
                ).order_by(desc("summ")).limit(first_of)
            else:
                result = db_session.query(
                    CategoryORM.name,
                    func.sum(GoodsORM.price_after_vat).label("summ")
                ).join(
                    GoodsORM.bill
                ).join(
                    GoodsORM.user_product
                ).join(
                    UserProductORM.categories
                ).filter(
                    CategoryORM.user_id == user_id,
                    GoodsORM.user_id == user_id,
                ).group_by(
                    CategoryORM.name
                ).order_by(desc("summ")).limit(first_of)
        else:
            if delta_month != 1:
                prev_month_date = get_fisrt_day_month_by_delta_month(
                    delta_month
                )
                logger.info(f"prev_month_date: {prev_month_date}")
                next_month_date = get_last_day_of_month_by_datetime(
                    prev_month_date
                )
                logger.info(f"next_month_date: {next_month_date}")
                result = db_session.query(
                    CategoryORM.name,
                    func.sum(GoodsORM.price_after_vat).label("summ")
                ).join(
                    GoodsORM.bill
                ).join(
                    GoodsORM.user_product
                ).join(
                    UserProductORM.categories
                ).filter(
                    CategoryORM.user_id == user_id,
                    GoodsORM.user_id == user_id,
                    BillORM.created >= prev_month_date,
                    BillORM.created <= next_month_date
                ).group_by(
                    CategoryORM.name
                ).order_by(desc("summ")).all()
            else:
                result = db_session.query(
                    CategoryORM.name,
                    func.sum(GoodsORM.price_after_vat).label("summ")
                ).join(
                    GoodsORM.bill
                ).join(
                    GoodsORM.user_product
                ).join(
                    UserProductORM.categories
                ).filter(
                    CategoryORM.user_id == user_id,
                    GoodsORM.user_id == user_id,
                ).group_by(
                    CategoryORM.name
                ).order_by(desc("summ")).all()
        return result


class CategoryCommands:

    def __init__(self):
        pass

    async def get_by_name(
        self, incoming_item: CategoryCreate
    ) -> Category:
        cat = CategoryORM.query.filter(
            CategoryORM.name == incoming_item.name,
            CategoryORM.user_id == incoming_item.user_id
        ).first()
        logger.info(f"cat: {cat}")
        return cat

    async def get_or_create(
        self, incoming_item: CategoryCreate, user_id: UUID
    ) -> Category:
        cat = await self.get_by_name(
            incoming_item=incoming_item
        )
        if not cat:
            cat = await self.create_category(
                incoming_item=incoming_item
            )
        return cat

    async def create_category(
        self, incoming_item: CategoryCreate
    ) -> Category:
        logger.info(f"incoming_item: {incoming_item}")
        incoming_item_dict = incoming_item.dict()
        cat = CategoryORM(**incoming_item_dict)
        db_session.add(cat)
        db_session.commit()
        logger.info(f"cat: {cat}")
        return cat

    async def update_category(
        self, incoming_item: CategoryUpdate
    ) -> Category:
        found_cat = CategoryORM.query.get(incoming_item.id)
        incoming_item_dict = incoming_item.dict()
        for key, value in incoming_item_dict.items():
            if value != None:
                setattr(found_cat, key, value)
        db_session.commit()
        return found_cat

    async def delete_category(
        self, id: UUID
    ) -> Category:
        cat = CategoryORM.query.filter_by(
            id=id
        ).first()
        db_session.delete(cat)
        db_session.commit()
        return cat
