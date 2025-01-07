from uuid import UUID
from loguru import logger

from ....app.login_link import LoginLinkCommands



"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# -------Views---------


# async def get_all_units() -> List[Unit]:
#     unit_views: UnitQueries = UnitQueries()
#     return await unit_views.get_all_units()


# async def get_unit(id: UUID) -> Unit:
#     unit_views: UnitQueries = UnitQueries()
#     return await unit_views.get_unit(id=id)


# --------Actions (commands) ---------


def countdown_deleting_login_link(id: UUID) -> bool:
    logger.info(f"id: {id}")
    login_link_commands = LoginLinkCommands()
    result = False
    command_result = login_link_commands.countdown_deleting(id=id)
    if command_result:
        result = True
    return result
