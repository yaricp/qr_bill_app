from uuid import UUID
from typing import List, MutableSequence

from fastapi import APIRouter

from ....domain.entities.user_entity import UserEntity

from ..services.user import (
    get_all_users,
    get_or_create_user
)


router = APIRouter()


@router.get("/", response_model=List[UserEntity])
async def read_users_route():
    """
    Retrieve users.
    """
    users: MutableSequence[UserEntity] = await get_all_users()
    return users


@router.get("/get_or_create/{id}", response_model=UserEntity)
async def get_or_create_user_route(id: UUID):
    user: UserEntity = await get_or_create_user(user_id=id)
    return user
