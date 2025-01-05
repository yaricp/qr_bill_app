import time
from datetime import datetime
from uuid import UUID
from loguru import logger

from ..app.config import login_link_config
from ..infra.database import db_session
from ..infra.database.models import LoginLink as LoginLinkORM


# class UnitQueries:

#     def __init__(self):
#         pass

#     async def get_all_units(self):
#         return UnitORM.query.all()

#     async def get_unit(self, id: UUID):
#         return UnitORM.query.get(id)


class LoginLinkCommands:

    def __init__(self):
        pass

    def countdown_deleting(self, id: UUID) -> bool:
        delta_conf = login_link_config.TIME_LIFE_TEMP_LOGIN_LINK_MIN
        time.sleep(delta_conf * 60)
        db_login_link = LoginLinkORM.query.get(id=id)
        if db_login_link:
            current_delta = (
                datetime.now() - db_login_link.created
            ).minutes
            if current_delta < delta_conf:
                time.sleep(1)
        self.delete(id=id)
        logger.info(f"Login link with {id} deleted")
        return True

    def delete(self, id: UUID):
        login_link = LoginLinkORM.query.delete(id=id)
        db_session.commit()
        return login_link
