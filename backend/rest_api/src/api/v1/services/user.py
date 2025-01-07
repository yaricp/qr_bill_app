from uuid import UUID
from typing import List
from loguru import logger


from ....app.user import (
    UserViews, UserQueries, UserCommands
)

from ... import manager
from ..schemas.user import User, UserCreate, UserUpdate

"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# -------Views---------


@manager.user_loader()
def check_user_auth(email_login_tg: str) -> User:
    logger.info(f"email_login_tg: {email_login_tg}")
    users_queries: UserQueries = UserQueries()
    if email_login_tg.find("@") != -1:
        logger.info("try search by email")
        user = users_queries.get_user_by_email(email_login_tg)
        logger.info(f"found by email: {user}")
        if user:
            return user
    logger.info("Try search user by tg_id")
    user = users_queries.get_user_by_tg_id(
        tg_id=email_login_tg
    )
    if user:
        return user
    return users_queries.get_user_by_login(
        login=email_login_tg
    )


def load_user(email_or_link: str) -> User:
    logger.info(f"email_or_link: {email_or_link}")
    users_queries: UserQueries = UserQueries()
    user = users_queries.get_user_by_login_link(
        link=email_or_link
    )
    if user:
        return user
    return users_queries.get_user_by_email(email_or_link)


async def get_user_by_login_link(link: str) -> User:
    users_queries: UserQueries = UserQueries()
    return await users_queries.get_user_by_login_link(link)


async def get_all_users() -> List[User]:
    users_queries: UserQueries = UserQueries()
    return await users_queries.get_all_users()


# --------Actions (commands) ---------


async def register_new_user(user_data: UserCreate) -> User:
    user_commands: UserCommands = UserCommands()
    command_result = await user_commands.register_user(
        user_data=user_data
    )
    return command_result
