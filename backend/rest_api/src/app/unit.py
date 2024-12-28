from uuid import UUID
from loguru import logger

from ..infra.database import db_session
from ..infra.database.models import Unit as UnitORM

from .entities.unit import Unit, UnitCreate


class UnitViews:

    def __init__(self):
        pass

    def some(self):
        pass


class UnitQueries:

    def __init__(self):
        pass

    async def get_all_units(self):
        return UnitORM.query.all()

    async def get_unit(self, id: UUID):
        return UnitORM.query.get(id)


class UnitCommands:

    def __init__(self):
        pass

    async def get_by_name(self, incoming_item: UnitCreate) -> Unit:
        unit = UnitORM.query.filter(
            UnitORM.name == incoming_item.name
        ).first()
        logger.info(f"unit: {unit}")
        return unit

    async def get_or_create(self, incoming_item: UnitCreate) -> Unit:
        seller = await self.get_by_name(
            incoming_item=incoming_item
        )
        if not seller:
            seller = await self.create_unit(
                incoming_item=incoming_item
            )
        return seller

    async def create_unit(self, incoming_item: UnitCreate) -> Unit:
        logger.info(f"incoming_item: {incoming_item}")
        incoming_item_dict = incoming_item.dict()
        unit = UnitORM(**incoming_item_dict)
        db_session.add(unit)
        db_session.commit()
        logger.info(f"unit: {unit}")
        return unit

    def update_unit(self):
        pass

    def delete_unit(self, id: UUID):
        pass
