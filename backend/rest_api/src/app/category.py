from uuid import UUID
from datetime import datetime
from loguru import logger

from ..infra.database import db_session
from ..infra.database.models import Category as CategoryORM

from .entities.category import (
    Category, CategoryCreate, CategoryUpdate
)


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
        ).delete()
        db_session.commit()
        return cat
