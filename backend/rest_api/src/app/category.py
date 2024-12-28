from uuid import UUID
from datetime import datetime
from loguru import logger

from ..infra.database import db_session
from ..infra.database.models import Category as CategoryORM


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

    def create_attraction(self):
        pass

    def update_attraction(self):
        pass

    def delete_attraction(self):
        pass
