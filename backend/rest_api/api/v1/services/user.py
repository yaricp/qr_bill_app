from uuid import UUID
from typing import List

from ....domain.entities.user_entity import (
    UserEntity
)

from ....app.queries.user_queries import UsersQuery


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# -------Views---------


async def get_all_users() -> List[UserEntity]:
    users_views: UsersQuery = UsersQuery()
    return await users_views.get_all_users()


# --------Actions (commands) ---------


async def get_or_create_user(user_id: UUID) -> UserEntity:
    user_queries = UsersQuery()
    command_result = await user_queries.get_or_create_user(
        user_id=user_id
    )
    return command_result
