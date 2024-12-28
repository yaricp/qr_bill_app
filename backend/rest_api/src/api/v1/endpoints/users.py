from uuid import UUID
from typing import List, MutableSequence

from fastapi import APIRouter

from ..services.user import (
    get_all_users,
    get_or_create_user
)
from ..schemas.user import User

router = APIRouter()


@router.get("/", response_model=List[User])
async def read_users_route():
    """
    Retrieve users.
    """
    users: MutableSequence[User] = await get_all_users()
    return users


@router.get("/get_or_create/{id}", response_model=User)
async def get_or_create_user_route(id: UUID):
    user: User = await get_or_create_user(user_id=id)
    return user
