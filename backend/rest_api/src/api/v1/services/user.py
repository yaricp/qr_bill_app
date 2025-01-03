from uuid import UUID
from typing import List


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
def load_user(email: str) -> User:
    if email == "admin":
        return User(
            id=UUID("0858baa8-1913-4fec-86ca-ca72b2f407a5"),
            email="admin",
            password_hash="8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
        )
    users_queries: UserQueries = UserQueries()
    return users_queries.get_user_by_email(email)


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
