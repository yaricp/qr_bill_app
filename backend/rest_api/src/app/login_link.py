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
        logger.info(f"delta_conf {delta_conf}")
        time.sleep(delta_conf * 60)
        logger.info("after sleep")
        db_login_link = LoginLinkORM.query.get(id)
        if db_login_link:
            current_delta = int(
                (datetime.now() - db_login_link.created).total_seconds()
            )
            if current_delta < delta_conf:
                logger.info("sleep again but just 1 min")
                time.sleep(1)
        self.delete(id=id)
        logger.info(f"Login link with {id} deleted")
        return True

    def delete(self, id: UUID):
        login_link = LoginLinkORM.query.get(id)
        if login_link:
            db_session.delete(login_link)
            db_session.commit()
        return login_link
