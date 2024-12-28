from uuid import UUID
from datetime import datetime
from loguru import logger

from ..infra.database import db_session
from ..infra.database.models import Category as CategoryORM

from .entities.category import (
    Category, CategoryCreate, CategoryUpdate
)


class CategoryViews:

    def __init__(self):
        pass

    def get_all_categories(self):
        pass


class CategoryQueries:

    def __init__(self):
        pass

    async def get_all_categories(self):
        return CategoryORM.query.all()

    async def get_category(self, id: UUID):
        return CategoryORM.query.get(id)


class CategoryCommands:

    def __init__(self):
        pass

    async def get_by_name(self, incoming_item: CategoryCreate) -> Category:
        cat = CategoryORM.query.filter(
            CategoryORM.name == incoming_item.name
        ).first()
        logger.info(f"cat: {cat}")
        return cat

    async def get_or_create(self, incoming_item: CategoryCreate) -> Category:
        cat = await self.get_by_name(
            incoming_item=incoming_item
        )
        if not cat:
            cat = await self.create_category(
                incoming_item=incoming_item
            )
        return cat

    async def create_category(self, incoming_item: CategoryCreate) -> Category:
        logger.info(f"incoming_item: {incoming_item}")
        incoming_item_dict = incoming_item.dict()
        cat = CategoryORM(**incoming_item_dict)
        db_session.add(cat)
        db_session.commit()
        logger.info(f"cat: {cat}")
        return cat

    def update_category(self, incoming_item: CategoryUpdate):
        pass

    def delete_category(self, id: UUID):
        pass
