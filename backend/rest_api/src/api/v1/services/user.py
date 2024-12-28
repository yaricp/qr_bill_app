from uuid import UUID
from typing import List


from ....app.user import UserViews, UserQueries, UserCommands

from ..schemas.user import User, UserCreate, UserUpdate

"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# -------Views---------


async def get_all_users() -> List[User]:
    users_views: UserViews = UserViews()
    return await users_views.get_all_users()


# --------Actions (commands) ---------


async def get_or_create_user(user_id: UUID) -> User:
    user_queries = UserQueries()
    command_result = await user_queries.get_or_create_user(
        user_id=user_id
    )
    return command_result
